from typing import Dict


def allow(reason=None) -> Dict:
    return {
        "allowed": True,
        "action": "allow",
        "risk_level": "low",
        "reason": reason
    }


def block(reason: str) -> Dict:
    return {
        "allowed": False,
        "action": "block",
        "risk_level": "high",
        "reason": reason
    }


def redirect(reason: str) -> Dict:
    return {
        "allowed": False,
        "action": "redirect",
        "risk_level": "medium",
        "reason": reason
    }