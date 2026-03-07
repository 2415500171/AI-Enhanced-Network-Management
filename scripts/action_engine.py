# Maps AI model output → automated network actions

ACTION_MAP = {
    0: {
        "status": "Normal",
        "action": "No action required. Network operating nominally.",
        "color": "green"
    },
    1: {
        "status": "Congested",
        "action": "AUTO-ACTION: Rerouting traffic to secondary path. "
                  "Load balancer threshold lowered to 60%.",
        "color": "orange"
    },
    2: {
        "status": "Under Attack",
        "action": "AUTO-ACTION: Activating firewall rules. "
                  "Flagging source IPs. Alerting security team.",
        "color": "red"
    }
}

def get_action(model_prediction: int) -> dict:
    return ACTION_MAP.get(model_prediction, ACTION_MAP[0])