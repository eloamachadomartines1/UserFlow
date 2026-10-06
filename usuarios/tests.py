from django.test import TestCase
from django.contrib.auth.models import User
from usuarios.forms import UsuarioModelForm
from usuarios.models import Usuario

class UsuarioFormTest(TestCase):

    def test_cpf_invalido_e_rejeitado(self):
        dados = {
            'nome': 'Teste da Silva',
            'cpf': '123', #CPF importado com 3 numeros
            'data_nascimento': '2000-01-01',
            'sexo': 'M',
        }
        form = UsuarioModelForm(data=dados)

        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)


    def test_cpf_valido_e_aceito(self):
        dados = {
            'nome': 'Maria Souza',
            'cpf': '12345678901', #11 numeros validos
            'data_nascimento': '1995-04-20',
            'sexo': 'F',
        }
        form = UsuarioModelForm(data=dados)

        self.assertTrue(form.is_valid())



class UsuarioViewTest(TestCase):

    def test_raiz_redireciona_para_login(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/usuarios/login/')

    def test_usuario_deslogado_não_acessa_listagem(self):
        response = self.client.get('/usuarios/')  
        self.assertRedirects(response, '/usuarios/login/?next=/usuarios/')

    def test_usuario_logado_acessa_listagem(self):
        User.objects.create_user(username='testeuser', password='senha123')
        self.client.login(username='testeuser', password='senha123')

        response = self.client.get('/usuarios/')

        self.assertEqual(response.status_code, 200)

    def test_usuario_deslogado_nao_acessa_criar(self):
        response = self.client.get('/usuarios/novo/')
        self.assertEqual(response.status_code, 302)


    def test_exclusao_faz_soft_delete(self):
        #Cria uma conta de login para simular um usuario autenticado
        User.objects.create_user(username='testeuser', password='senha123')
        self.client.login(username='testeuser', password='senha123')

        usuario = Usuario.objects.create(
            nome='Eloá M.',
            cpf='98765432100',
            data_nascimento='2010-07-15',
            sexo='M',
        )

        self.client.post(f'/usuarios/excluir/{usuario.pk}/')

        usuario.refresh_from_db()

        self.assertFalse(usuario.ativo)