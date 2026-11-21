"""Visualizador interativo do planeta Terra em 3D usando PyVista.

Na primeira execução, o PyVista baixa e armazena em cache a malha e a
textura do globo. Depois disso, os arquivos ficam disponíveis localmente.
"""

from __future__ import annotations

import sys

import pyvista as pv


TITULO_JANELA = "Globo Terrestre 3D - PyVista"
TAMANHO_JANELA = (1280, 850)
COR_FUNDO = "#030712"


def carregar_terra() -> tuple[pv.PolyData, pv.Texture]:
    """Carrega a malha esférica e a textura terrestre fornecidas pelo PyVista."""
    try:
        globo = pv.examples.load_globe()
        textura = pv.examples.load_globe_texture()
        return globo, textura
    except Exception as erro:
        print("\nNão foi possível carregar os dados do globo terrestre.\n")
        print("Na primeira execução, o PyVista precisa acessar a internet para")
        print("baixar a malha 3D e a imagem de textura da Terra.")
        print("\nVerifique sua conexão e tente executar o programa novamente.")
        print("\nDetalhes técnicos:")
        print(f"{type(erro).__name__}: {erro}")
        raise SystemExit(1) from erro


def criar_janela(globo: pv.PolyData, textura: pv.Texture) -> pv.Plotter:
    """Monta a cena 3D e configura os controles de visualização."""
    plotter = pv.Plotter(
        window_size=TAMANHO_JANELA,
        title=TITULO_JANELA,
    )
    plotter.set_background(COR_FUNDO)

    # Calcula o raio a partir dos limites reais da malha carregada.
    limites = globo.bounds
    raio = max(
        limites[1] - limites[0],
        limites[3] - limites[2],
        limites[5] - limites[4],
    ) / 2.0

    # Camada atmosférica sutil, ligeiramente maior que a superfície terrestre.
    atmosfera = pv.Sphere(
        radius=raio * 1.012,
        center=globo.center,
        theta_resolution=160,
        phi_resolution=160,
    )
    plotter.add_mesh(
        atmosfera,
        color="#4AA9FF",
        opacity=0.10,
        smooth_shading=True,
        lighting=False,
        name="Atmosfera",
        reset_camera=False,
    )

    # Superfície da Terra com textura de mapa-múndi em alta definição.
    plotter.add_mesh(
        globo,
        texture=textura,
        smooth_shading=True,
        ambient=0.32,
        diffuse=0.78,
        specular=0.18,
        specular_power=24,
        name="Planeta Terra",
        reset_camera=False,
    )

    # Identificação e instruções dentro da própria janela 3D.
    plotter.add_text(
        "PLANETA TERRA",
        position="upper_left",
        font_size=17,
        color="white",
        font="arial",
        shadow=True,
    )
    plotter.add_text(
        "VISUALIZACAO TRIDIMENSIONAL",
        position=(18, 42),
        font_size=9,
        color="#8FBCEB",
        font="arial",
    )
    plotter.add_text(
        "Mouse esquerdo: girar   |   Roda do mouse: aproximar/afastar\n"
        "Botao direito: deslocar   |   Tecla R: redefinir a camera",
        position="lower_left",
        font_size=10,
        color="#D1D5DB",
        font="arial",
    )

    # Posiciona a câmera e aproxima um pouco o globo.
    plotter.view_isometric()
    plotter.reset_camera()
    plotter.camera.zoom(1.22)

    def redefinir_camera() -> None:
        plotter.view_isometric()
        plotter.reset_camera()
        plotter.camera.zoom(1.22)
        plotter.render()

    plotter.add_key_event("r", redefinir_camera)
    plotter.add_key_event("R", redefinir_camera)

    return plotter


def main() -> None:
    print("Carregando o globo terrestre 3D...")
    globo, textura = carregar_terra()

    plotter = criar_janela(globo, textura)
    print("Globo carregado. Feche a janela 3D para encerrar o programa.")
    plotter.show()


if __name__ == "__main__":
    main()
