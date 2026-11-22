"""Read an OpenHands conversation ZIP without extraction or printing secrets.

Usage: python analyze_openhands_export.py conversation.zip --output summary.json
Only validated for the Agent Canvas export inspected on 2026-11-22.
Missing metrics remain null; recorded responses are not total API attempts.
"""
import argparse
import collections
import datetime as dt
import json
import pathlib
import zipfile


def analyze(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        states = [n for n in names if n.endswith('/base_state.json')]
        if len(states) != 1:
            raise ValueError('Expected exactly one conversation base_state.json')
        prefix = states[0].removesuffix('base_state.json')
        def read(name):
            return json.loads(archive.read(prefix + name))
        state = read('base_state.json')
        meta = read('meta.json')
        events = [json.loads(archive.read(n)) for n in sorted(names)
                  if n.startswith(prefix + 'events/event-') and n.endswith('.json')]
        unique = {e['id']: e for e in events}
        if len(unique) != len(events):
            raise ValueError('Duplicate event IDs: inspect before counting')
        actions = [e for e in events if e.get('kind') == 'ActionEvent']
        observations = [e for e in events if e.get('kind') == 'ObservationEvent']
        human_messages = [e for e in events if e.get('kind') == 'MessageEvent'
                          and e.get('source') == 'user']
        interrupts = [e for e in events if e.get('kind') == 'InterruptEvent'
                      and e.get('source') == 'user']
        agent_messages = [e for e in events if e.get('kind') == 'MessageEvent'
                          and e.get('source') == 'agent']
        buckets = state.get('stats', {}).get('usage_to_metrics')
        metrics = []
        if isinstance(buckets, dict):
            for usage_id, bucket in buckets.items():
                # Read ONE final snapshot. Never add event snapshots to this.
                token_records = bucket.get('token_usages')
                response_ids = sorted({r['response_id'] for r in token_records or []
                                       if r.get('response_id')})
                metrics.append({
                    'usage_id': usage_id,
                    'model': bucket.get('model_name'),
                    'recorded_response_ids': response_ids,
                    'recorded_responses_with_id': len(response_ids),
                    'token_usage_records': len(token_records) if isinstance(token_records, list) else None,
                    'tokens_final_snapshot': bucket.get('accumulated_token_usage'),
                    'reported_accumulated_cost': bucket.get('accumulated_cost'),
                    'currency_explicit_in_export': bucket.get('currency'),
                    'response_latencies': bucket.get('response_latencies'),
                })
        def timestamp(e):
            # Export timestamps have no offset. Differences are still measurable.
            return dt.datetime.fromisoformat(e['timestamp'])
        running_at = None
        intervals = []
        for event in events:
            if event.get('kind') != 'ConversationStateUpdateEvent' or event.get('key') != 'execution_status':
                continue
            value = event.get('value')
            if value == 'running' and running_at is None:
                running_at = timestamp(event)
            elif value != 'running' and running_at is not None:
                intervals.append((timestamp(event) - running_at).total_seconds())
                running_at = None
        tools = [t.get('name') for t in state.get('agent', {}).get('tools', [])]
        delegation_names = {'task_tool_set', 'task', 'delegate', 'launch_child_conversation'}
        prompt_toolsets = [e.get('tools', []) for e in events if e.get('kind') == 'SystemPromptEvent']
        prompt_tools = sorted({t.get('name') or t.get('title') or t.get('client_tool_name')
                               for ts in prompt_toolsets for t in ts
                               if t.get('name') or t.get('title') or t.get('client_tool_name')})
        client_tools = [t.get('name') for t in meta.get('client_tools', [])]
        exposed_delegation = delegation_names.intersection(tools + prompt_tools + client_tools)
        errors = [e for e in events if e.get('kind') == 'ConversationErrorEvent']
        llm = state.get('agent', {}).get('llm', {})
        return {
            'conversation_id': state.get('id'),
            'phase': 'setup_trial_not_experiment',
            'execution_status': state.get('execution_status'),
            'event_count': len(events),
            'events_by_kind': dict(collections.Counter(e.get('kind') for e in events)),
            'agent_action_events': len(actions),
            'agent_message_events': len(agent_messages),
            'actions_by_tool': dict(collections.Counter(e.get('tool_name') for e in actions)),
            'observation_events': len(observations),
            'human_message_events': len(human_messages),
            'human_interrupt_events': len(interrupts),
            'pause_events_separate_from_InterruptEvent': sum(e.get('kind') == 'PauseEvent' for e in events),
            'M20_interventions': None,
            'M20_note': 'Classify messages, interruptions and external configuration changes in milestone diary; initial brief is separate. This is preparation only.',
            'model': llm.get('model'),
            'llm_settings': {k: llm.get(k) for k in ['num_retries', 'timeout', 'stream', 'stream_idle_timeout', 'log_completions']},
            'available_tools': tools,
            'system_prompt_tools': prompt_tools,
            'client_tools': client_tools,
            'delegation_tools_available': sorted(exposed_delegation),
            'delegation_action_events': sum(e.get('tool_name') in delegation_names for e in actions),
            'single_agent_configuration_verified': False if exposed_delegation else (True if prompt_toolsets else None),
            'security_analyzer_kind': (state.get('security_analyzer') or {}).get('kind'),
            'autotitle': meta.get('autotitle'),
            'model_metrics': metrics if buckets is not None else None,
            'total_model_api_attempts': None,
            'actual_billed_cost': None,
            'verified_total_tokens_including_failed_or_interrupted_requests': None,
            'error_events': [{'id': e['id'], 'code': e.get('code'),
                              'contains_503': '503' in str(e.get('detail', '')),
                              'contains_429': '429' in str(e.get('detail', ''))} for e in errors],
            'event_span_seconds': (timestamp(events[-1]) - timestamp(events[0])).total_seconds() if len(events) > 1 else None,
            'completed_running_intervals_seconds': intervals,
            'running_intervals_total_seconds': sum(intervals) if intervals and running_at is None else None,
            'open_running_interval': running_at is not None,
            'bash_command_log_entries_not_agent_steps': sum('/bash_events/' in n and '_BashCommand_' in n for n in names),
            'notes': [
                'Counts apply to this one exported conversation only, not other conversations or provider logs.',
                'ActionEvent count is a tool-action definition of agent steps, not model calls or shell command count.',
                'Error events may describe the same failure; do not count them as API attempts.',
                'Successful response IDs omit failed attempts, retries, interrupted streams and potentially auxiliary calls.',
                'Zero values in tokens_final_snapshot are raw SDK counters, not proof that failed or interrupted requests consumed zero tokens.',
                'Tool-policy verification excludes known built-in delegation tools; it is not an OS-level ban on arbitrary processes or network calls through terminal.',
                'Reasoning tokens are reported separately; do not add them to completion_tokens without checking provider semantics.',
                'Reported cost is not a billing receipt and may use public list prices even on a free-tier account.',
                'Running intervals include tool execution, model waits and retries, not only generation time.',
                'Raw ZIP may contain credentials and private data. This report emits neither prompts nor secret values.',
            ],
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('zip_path', type=pathlib.Path)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    report = analyze(args.zip_path)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Wrote sanitized summary:', args.output)
