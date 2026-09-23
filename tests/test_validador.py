import unittest
from src import ValidadorInteligente

class TestValidadorInteligente(unittest.TestCase):
    def setUp(self):
        self.validador = ValidadorInteligente()

    def test_email_typo_sugiere_correccion(self):
        r = self.validador.validar_campo("email", "persona@gamil.com", "T-01", "web_form")
        self.assertIn("typo_dominio_comun", r["errores"])
        self.assertEqual(r["accion"], "sugerir_correccion")

    def test_telefono_sin_pais_pide_confirmacion(self):
        r = self.validador.validar_campo("telefono", "1155555555", "T-02", "whatsapp")
        self.assertIn("telefono_sin_codigo_pais", r["errores"])
        self.assertEqual(r["accion"], "confirmar_por_fuente_o_llamada")

    def test_empresa_conocida_es_aceptada(self):
        r = self.validador.validar_campo("empresa", "TechCorp S.A.", "T-03", "web_form")
        self.assertTrue(r["valido"])

if __name__ == "__main__":
    unittest.main()
