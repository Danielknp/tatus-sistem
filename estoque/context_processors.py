from django.utils.timezone import now

def sessao_expira_em(request):
    if request.user.is_authenticated:
        # Pega a data de expiração da sessão
        expiracao = request.session.get_expiry_date()
        # Converte para timestamp (segundos desde 1970)
        timestamp = int(expiracao.timestamp())
        return {'sessao_expira_em': timestamp}
    return {'sessao_expira_em': None}