"""Create an EMPTY single-agent trial using the existing local OpenHands profile.

No initial message, no provider key handling, no Gemini request. Uses the local
session key intentionally embedded by the localhost-only Agent Canvas launcher.
Validated with Canvas 1.43.0 / agent-server 1.63.1. Do not expose this server.
"""
import argparse
import json
import pathlib
import re
import urllib.error
import urllib.request
import uuid

BASE = 'http://127.0.0.1:8000'
FORBIDDEN = {'task_tool_set', 'task', 'delegate', 'launch_child_conversation',
             'switch_llm', 'classify_and_switch_llm'}
EXPECTED = {'file_editor', 'task_tracker', 'terminal', 'browser_tool_set'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fail-fast', action='store_true',
                        help='Materialize the same profile, disable streaming/retries, and use a 45-second timeout for diagnostics.')
    parser.add_argument('--output', type=pathlib.Path,
                        default=pathlib.Path(__file__).with_name('single-agent-trial-proof.json'))
    args = parser.parse_args()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    html = opener.open(BASE + '/canvas/', timeout=15).read().decode('utf-8')
    match = re.search(r'window\.__AGENT_CANVAS_SESSION_API_KEY__\s*=\s*("(?:[^"\\]|\\.)*")', html)
    if not match:
        raise RuntimeError('Local session-key bootstrap is unavailable; no changes made.')
    session_key = json.loads(match.group(1))
    if not isinstance(session_key, str) or not session_key:
        raise RuntimeError('No local session key; no changes made.')

    def api(path, method='GET', payload=None, headers_override=None):
        request = urllib.request.Request(
            BASE + path, method=method,
            headers={'X-Session-API-Key': session_key, 'Content-Type': 'application/json',
                     **(headers_override or {})},
            data=json.dumps(payload).encode('utf-8') if payload is not None else None)
        try:
            with opener.open(request, timeout=60) as response:
                data = response.read()
                return json.loads(data) if data else None
        except urllib.error.HTTPError as error:
            # Do not echo server bodies; they can contain resolved credentials.
            raise RuntimeError(f'Local API returned HTTP {error.code} for {method} {path}') from None

    info = api('/server_info')
    if info.get('version') != '1.63.1':
        raise RuntimeError('Agent-server version changed; review API and tool policy before launching.')
    profile = api('/api/agent-profiles/default')['profile']
    tools = {tool['name'] for tool in profile.get('tools') or []}
    if profile.get('agent_kind') != 'openhands' or tools != EXPECTED:
        raise RuntimeError('The default profile does not have the audited explicit tool allowlist.')
    if profile.get('llm_profile_ref') != 'gemini-3.8-flash':
        raise RuntimeError('The default profile uses a different LLM profile.')
    if profile.get('condenser', {}).get('enabled') is not False:
        raise RuntimeError('Disable condensation for this short trial first.')
    verification = profile.get('verification') or {}
    if verification.get('critic_enabled') or verification.get('enable_iterative_refinement'):
        raise RuntimeError('Disable critic/refinement for this short trial first.')
    if profile.get('enable_classify_and_switch_llm_tool') or profile.get('meta_profile_ref'):
        raise RuntimeError('Model routing must be disabled for this trial.')
    if profile.get('tool_concurrency_limit') != 1:
        raise RuntimeError('Unexpected tool concurrency setting.')
    identity = str(uuid.uuid4())
    if args.output.exists():
        raise RuntimeError('Proof output already exists. Use another --output path; no new session created.')
    payload = {
        'conversation_id': identity,
        'agent_profile_id': profile['id'],
        'workspace': {'kind': 'LocalWorkspace', 'working_dir': '/projects/variant-c'},
        'worktree': False,
        'client_tools': [],
        'agent_definitions': [],
        'plugins': [],
        'autotitle': False,
        'security_analyzer': None,
        'confirmation_policy': {'kind': 'NeverConfirm'},
        'max_iterations': 20,
        'stuck_detection': True,
        'tags': {'phase': 'setuptrial', 'policy': 'singleagentapi',
                 'clientsource': 'agentcanvas', 'workspace': '/projects/variant-c'},
    }
    if args.fail_fast:
        materialized = api('/api/agent-profiles/default/materialize', 'POST', {})
        if not materialized.get('valid'):
            raise RuntimeError('Stored profile cannot be materialized; no new session created.')
        settings = materialized['resolved_settings']
        # Credentials travel only over the existing authenticated loopback API.
        # They remain in memory and are never included in the proof file/stdout.
        config = api('/api/profiles/gemini-3.8-flash',
                     headers_override={'X-Expose-Secrets': 'plaintext'})['config']
        if config.get('model') != 'gemini/gemini-3.8-flash':
            raise RuntimeError('Resolved LLM profile has changed model.')
        config.update(stream=False, num_retries=0, timeout=45, stream_idle_timeout=30)
        settings['llm'] = config
        del payload['agent_profile_id']
        payload['agent_settings'] = settings
    public_payload = dict(payload)
    if args.fail_fast:
        public_payload['agent_settings'] = {
            'source': 'Materialized default profile, credentials omitted',
            'tools': settings['tools'],
            'llm': {name: config.get(name) for name in
                    ['model', 'stream', 'num_retries', 'timeout', 'stream_idle_timeout', 'reasoning_effort']},
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Minimal recovery record contains no secrets; retained even if verification fails.
    args.output.write_text(json.dumps({'conversation_id': identity, 'verified': False,
                                      'creation_request_without_secrets': public_payload}, indent=2), encoding='utf-8')
    api('/api/conversations', 'POST', payload)
    api('/api/conversations/' + identity, 'PATCH', {'title': 'SETUP: single-agent verification'})
    actual = api('/api/conversations/' + identity)
    agent = actual.get('agent') or {}
    actual_tools = [tool['name'] for tool in agent.get('tools') or []]
    if set(actual_tools) != EXPECTED or FORBIDDEN.intersection(actual_tools):
        raise RuntimeError('Created session failed tool verification. Do not send it a message; see proof file for its ID.')
    if (agent.get('llm') or {}).get('model') != 'gemini/gemini-3.8-flash':
        raise RuntimeError('Created session resolved to a different model. Do not send it a message.')
    if args.fail_fast:
        for name, value in {'stream': False, 'num_retries': 0, 'timeout': 45, 'stream_idle_timeout': 30}.items():
            if agent['llm'].get(name) != value:
                raise RuntimeError('Server changed a diagnostic transport setting. Do not run this session.')
    proof = {
        'conversation_id': identity,
        'url': f'http://localhost:8000/canvas/conversations/{identity}',
        'verified': True,
        'verification_scope': 'Empty session configuration; repeat inspection after UI attachment and after a trial run.',
        'phase': 'setup_trial_not_experiment',
        'agent_server_version': info.get('version'),
        'sdk_version': info.get('sdk_version'),
        'profile_id': profile['id'],
        'profile_revision': profile.get('revision'),
        'available_tools': actual_tools,
        'forbidden_tools_present': sorted(FORBIDDEN.intersection(actual_tools)),
        'model': (agent.get('llm') or {}).get('model'),
        'autotitle_requested': False,
        'security_analyzer_requested': None,
        'initial_message_sent': False,
        'max_iterations': 20,
        'execution_status': actual.get('execution_status'),
        'creation_request_without_secrets': public_payload,
        'transport_mode': 'fail-fast non-streaming' if args.fail_fast else 'profile defaults',
        'note': 'Browser, profile, tools or future version changes require another configuration audit. Runtime API/terminal capabilities are not an OS-level prohibition on all possible child processes.',
    }
    args.output.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Verified EMPTY trial session; no initial model request sent.')
    print(proof['url'])
    print('Tools:', ', '.join(actual_tools))
    print('Proof:', args.output)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('STOP:', str(error))
        raise SystemExit(1)
