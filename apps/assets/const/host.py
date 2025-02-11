from .base import BaseType

GATEWAY_NAME = 'Gateway'


class HostTypes(BaseType):
    LINUX = 'linux', 'Linux'
    WINDOWS = 'windows', 'Windows'
    UNIX = 'unix', 'Unix'
    OTHER_HOST = 'other', "Other"

    @classmethod
    def _get_base_constrains(cls) -> dict:
        return {
            '*': {
                'charset_enabled': True,
                'charset': 'utf-8',  # default
                'domain_enabled': True,
                'su_enabled': True,
                'su_methods': [
                    {'name': 'sudo su', 'id': 'sudo su'},
                    {'name': 'su -', 'id': 'su -'}
                ],
            },
            cls.WINDOWS: {
                'su_enabled': False,
            },
            cls.OTHER_HOST: {
                'su_enabled': False,
            }
        }

    @classmethod
    def _get_protocol_constrains(cls) -> dict:
        return {
            '*': {
                'choices': ['ssh', 'telnet', 'vnc', 'rdp']
            },
            cls.WINDOWS: {
                'choices': ['rdp', 'ssh', 'vnc']
            }
        }

    @classmethod
    def _get_automation_constrains(cls) -> dict:
        return {
            '*': {
                'ansible_enabled': True,
                'ansible_config': {
                    'ansible_connection': 'smart',
                },
                'ping_enabled': True,
                'gather_facts_enabled': True,
                'gather_accounts_enabled': True,
                'verify_account_enabled': True,
                'change_secret_enabled': True,
                'push_account_enabled': True
            },
            cls.WINDOWS: {
                'ansible_config': {
                    'ansible_shell_type': 'cmd',
                    'ansible_connection': 'ssh',
                },
            },
        }

    @classmethod
    def internal_platforms(cls):
        return {
            cls.LINUX: [
                {'name': 'Linux'},
                {'name': GATEWAY_NAME}
            ],
            cls.UNIX: [
                {'name': 'Unix'},
                {'name': 'macOS'},
                {'name': 'BSD'},
                {'name': 'AIX'},
            ],
            cls.WINDOWS: [
                {'name': 'Windows'},
                {
                    'name': 'Windows-TLS',
                    'protocols_setting': {
                        'rdp': {'security': 'tls'},
                    }
                },
                {
                    'name': 'Windows-RDP',
                    'protocols_setting': {
                        'rdp': {'security': 'rdp'},
                    }
                },
                {
                    'name': 'RemoteAppHost',
                    '_protocols': ['rdp', 'ssh'],
                    'protocols_setting': {
                        'ssh': {
                            'required': True
                        }
                    }
                }
            ],
            cls.OTHER_HOST: []
        }

    @classmethod
    def get_community_types(cls) -> list:
        return [
            cls.LINUX, cls.UNIX, cls.WINDOWS, cls.OTHER_HOST
        ]
