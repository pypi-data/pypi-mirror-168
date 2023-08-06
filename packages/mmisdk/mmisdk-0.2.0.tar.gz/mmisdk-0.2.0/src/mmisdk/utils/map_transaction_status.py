def map_transaction_status(status: str, reason: str):
    if status == 'created':
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Created',
            "reason": reason,
        }
    if status == 'pending':
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Pending',
            "reason": reason,
        }
    if status == 'authorized':
        return {
            "finished": False,
            "submitted": False,
            "signed": False,
            "success": False,
            "displayText": 'Authorized',
            "reason": reason,
        }
    if status == 'approved':
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
            "signed": False,
            "success": False,
            "displayText": 'Submitted',
            "reason": reason,
        }
    if status == 'mined':
        return {
            "finished": True,
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Mined',
            "reason": reason,
        }
    if status == 'completed':
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
            "submitted": True,
            "signed": True,
            "success": False,
            "displayText": 'Aborted',
            "reason": reason,
        }
    if status == 'rejected':
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
    if status == 'overriden':
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
