def map_transaction_status(status: str, reason: str):
    """
    Maps custodians' transaction statuses to JSON-RPC statuses, as documented in
    https://consensys.gitlab.io/codefi/products/mmi/mmi-docs/faq/transactions/?h=status#how-do-transaction-statuses-work

    Args:
        status: str - The transaction status string, in the custodian's nomenclature
        reason: Optional[str] - The reason for the signed message status, for instance "Signed message was rejected by the user", or "Signed message was cancelled by the user"
    Returns:
        A dictionary with the JSON-RPC status fields.
    """
    if status == 'created':
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Created',
            "reason": reason,
        }
    if status == 'pending':  # TODO TBC
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Pending',
            "reason": reason,
        }
    if status == 'authorized':  # TODO TBC
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Authorized',
            "reason": reason,
        }
    if status == 'approved':  # TODO TBC
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Created',
            "reason": reason,
        }
    if status == 'signed':
        return {
            "finished": False,
            "submitted": False,
            "signed": True,
            "success": False,
            "displayText": 'Signed',
            "reason": reason,
        }
    if status == 'submitted':
        return {
            "finished": False,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Submitted',
            "reason": reason,
        }
    if status == 'mined':
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": True,
            "displayText": 'Mined',
            "reason": reason,
        }
    if status == 'completed':  # TODO TBC
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Completed',
            "reason": reason,
        }
    if status == 'aborted':
        return {
            "finished": True,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Aborted',
            "reason": reason,
        }
    if status == 'rejected':  # TODO TBC
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Rejected',
            "reason": reason,
        }
    if status == 'failed':
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Failed',
            "reason": reason,
        }
    if status == 'overriden':  # TODO TBC
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Overriden',
            "reason": reason,
        }
    else:
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Unknown',
            "reason": reason,
        }
