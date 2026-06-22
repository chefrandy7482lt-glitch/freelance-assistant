from datetime import datetime
from typing import Dict, Any, List


class DomainRegistry:
    """
    TDU Domain Registry Layer

    This is the first structural layer of the ecosystem.
    It defines what systems exist and how they communicate.
    """

    def __init__(self):
        self.domains = {
            "freelance": {
                "status": "active",
                "description": "Freelance task and proposal system"
            },
            "pricing": {
                "status": "active",
                "description": "Value-based pricing engine"
            },
            "accounting": {
                "status": "inactive",
                "description": "Personal financial mapping layer"
            },
            "communication": {
                "status": "inactive",
                "description": "Client messaging and outreach layer"
            }
        }

        self.event_log: List[Dict[str, Any]] = []

    def register_event(self, domain: str, event: str, payload: Dict[str, Any]):
        """Logs a system event into the registry layer."""
        self.event_log.append({
            "domain": domain,
            "event": event,
            "payload": payload,
            "timestamp": str(datetime.now())
        })

    def get_domain_status(self, domain: str):
        return self.domains.get(domain, {"status": "unknown"})

    def activate_domain(self, domain: str):
        if domain in self.domains:
            self.domains[domain]["status"] = "active"
            self.register_event(domain, "activated", {})
            return True
        return False

    def list_domains(self):
        return self.domains

    def get_event_log(self):
        return self.event_log