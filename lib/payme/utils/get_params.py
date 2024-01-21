from django.conf import settings


def get_params(params: dict) -> dict:
    """
    Use this function to get the parameters from the payme.
    """
    account: dict = params.get("account")

    clean_params: dict = {}
    clean_params["_id"] = params.get("id")
    clean_params["time"] = params.get("time")
    clean_params["amount"] = params.get("amount")
    clean_params["reason"] = params.get("reason")

    # get statement method params
    clean_params["start_date"] = params.get("from")
    clean_params["end_date"] = params.get("to")

    if account is not None:
        account_name: str = settings.PAYME.get("PAYME_ACCOUNT")
        clean_params["order_id"] = account[account_name]

    return clean_params


def clean_empty(data) -> dict:
    """
    Use this function to clean the parameters from the instance.
    """
    if isinstance(data, dict):
        return {
            k: v
            for k, v in ((k, clean_empty(v)) for k, v in data.items())
            if v is not None and k != "id"
        }
    if isinstance(data, list):
        return [v for v in map(clean_empty, data) if v]

    return data
