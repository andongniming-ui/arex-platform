"""Cron expression validation utility."""
from croniter import croniter
from datetime import datetime


def validate_cron_expression(cron_expr: str) -> tuple[bool, str]:
    """
    Validate a cron expression.
    
    Args:
        cron_expr: Cron expression (5 fields: minute hour day month weekday)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not cron_expr:
        return False, "Cron expression cannot be empty"
    
    fields = cron_expr.strip().split()
    
    # Support both 5-field and 6-field cron
    if len(fields) not in (5, 6):
        return False, f"Invalid cron fields count: {len(fields)} (expected 5 or 6)"
    
    try:
        # Test if cron expression is valid
        cron = croniter(cron_expr)
        # Get next run to verify
        next_run = cron.get_next(datetime)
        return True, f"Next run: {next_run.isoformat()}"
    except Exception as e:
        return False, f"Invalid cron expression: {str(e)}"


def is_valid_cron(cron_expr: str) -> bool:
    """Quick check if cron expression is valid."""
    valid, _ = validate_cron_expression(cron_expr)
    return valid
