from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.http.request import split_domain_port


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        for remote_addr in x_forwarded_for.split(","):
            try:
                remote_addr = remote_addr.strip()
                remote_addr, _ = split_domain_port(remote_addr)
                validate_ipv46_address(remote_addr)
                return remote_addr
            except (ValidationError, TypeError):
                continue

    remote_addr = request.META.get("REMOTE_ADDR", "")
    try:
        remote_addr = remote_addr.strip()
        remote_addr, _ = split_domain_port(remote_addr)
        validate_ipv46_address(remote_addr)
        return remote_addr
    except (ValidationError, TypeError):
        return None
