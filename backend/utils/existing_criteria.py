from utils.models import Criteria

# existing criteria to start the graph state with
NETWORK_CRITERIA = [
    Criteria(
        title="backend_infrastructure",
        description="""This use case is for when the network is used to manage backend servers and databases. 
        This use case is appropriate for ensuring that database and backend API server requests are validated 
        and not coming from unauthorized or foreign locations.""",
        criteria={
            "protocols": ["TCP"],
            "ports": [
                3306,  # MySQL
                5432,  # PostgreSQL
                6379,  # Redis
                27017, # MongoDB
                8080,  # Common API port
                443    # HTTPS
            ],
            "ip_ranges": [
                "10.0.0.0/8",     # Internal network
                "172.16.0.0/12",  # Internal network
                "192.168.0.0/16"  # Internal network
            ],
            "track_fields": [
                "source_ip",
                "destination_ip",
                "transport_layer.protocol",
                "transport_layer.source_port",
                "transport_layer.destination_port",
                "transport_layer.flags",
                "payload.length"
            ],
            "alert_conditions": {
                "unauthorized_ip": "source_ip not in ip_ranges",
                "suspicious_ports": "destination_port not in ports",
                "large_payload": "payload.length > 1000000"
            }
        }
    ),
    Criteria(
        title="web_application",
        description="""This use case is for hosting and managing web applications that serve content to end users. 
        This includes monitoring HTTP/HTTPS traffic, managing user sessions, and detecting potential DDoS or web attacks.""",
        criteria={
            "protocols": ["TCP"],
            "ports": [
                80,   # HTTP
                443,  # HTTPS
                8080, # Alternative HTTP
                8443  # Alternative HTTPS
            ],
            "track_fields": [
                "transport_layer.protocol",
                "transport_layer.flags",
                "transport_layer.source_port",
                "transport_layer.destination_port",
                "application_layer.protocol",
                "source_ip",
                "payload.length"
            ],
            "alert_conditions": {
                "syn_flood": "COUNT(transport_layer.flags.syn) > 1000 per minute",
                "payload_size": "payload.length > 500000",
                "error_rate": "COUNT(application_layer.status_code >= 400) > 100 per minute"
            }
        }
    ),
    Criteria(
        title="general_usage",
        description="""This use case is for general internet usage including web browsing, email, and common 
        application traffic. This profile focuses on basic security monitoring and detecting unusual patterns 
        in regular internet usage.""",
        criteria={
            "protocols": ["TCP", "UDP"],
            "ports": [
                80,    # HTTP
                443,   # HTTPS
                53,    # DNS
                25,    # SMTP
                110,   # POP3
                143,   # IMAP
                587,   # SMTP (TLS)
                993,   # IMAPS
                995    # POP3S
            ],
            "track_fields": [
                "timestamp",
                "source_ip",
                "destination_ip",
                "transport_layer.protocol",
                "transport_layer.destination_port",
                "application_layer.protocol"
            ],
            "alert_conditions": {
                "unusual_port": "destination_port not in common_ports",
                "high_volume": "COUNT(packets) > 10000 per minute",
                "suspicious_dns": "COUNT(destination_port = 53) > 100 per minute"
            }
        }
    )
]