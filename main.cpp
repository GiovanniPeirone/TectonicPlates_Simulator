#include <SDL2/SDL.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <cstdlib>  // Para std::atoi

// Tamaño de la ventana
const int WINDOW_WIDTH = 1600;  // Aumentamos el ancho
const int WINDOW_HEIGHT = 1200; // Aumentamos la altura

// Tamaño de los "bloques" de terreno (en lugar de píxeles individuales)
const int BLOCK_SIZE = 10;  // Tamaño de cada bloque cuadrado

// Función para generar ruido de Perlin (implementación simple)
float perlinNoise(int x, int y) {
    // Función pseudoaleatoria simple
    static std::default_random_engine generator;
    static std::uniform_real_distribution<float> distribution(0.0, 1.0);
    return distribution(generator);
}

// Función para generar el mapa de alturas utilizando el ruido de Perlin
void generateTerrain(std::vector<std::vector<float>>& terrain, int width, int height, float scale) {
    // Generar dos islas grandes centradas a la izquierda y a la derecha
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            // Generamos dos islas usando desplazamientos
            float islandLeft = perlinNoise((x - width / 3) / scale, (y) / scale);  // Isla izquierda
            float islandRight = perlinNoise((x - 2 * width / 3) / scale, (y) / scale);  // Isla derecha
            
            // Mezclamos ambos valores de las islas
            float terrainHeight = std::max(islandLeft, islandRight);

            terrain[y][x] = terrainHeight;
        }
    }
}

// Función para renderizar el mapa con bloques más grandes
void renderMap(SDL_Renderer* renderer, const std::vector<std::vector<float>>& terrain, int blockSize) {
    // Iterar sobre el mapa de alturas y cambiar el color del terreno según la altura
    for (int y = 0; y < terrain.size(); y++) {
        for (int x = 0; x < terrain[y].size(); x++) {
            float height = terrain[y][x];

            // Normalizar la altura entre 0 y 1
            float normalizedHeight = std::min(1.0f, std::max(0.0f, height));

            // Usar una escala de colores para representar el terreno
            int red = 0;
            int green = 0;
            int blue = 255;

            if (normalizedHeight > 0.5f) {
                // Las islas tienen un color más verde/marrón
                green = std::min(255, static_cast<int>((normalizedHeight - 0.5f) * 2 * 255));
                blue = std::max(0, 255 - static_cast<int>((normalizedHeight - 0.5f) * 2 * 255));
            }

            if (normalizedHeight > 0.8f) {
                // Las zonas más altas (montañas) se vuelven marrones o grises
                red = std::min(255, static_cast<int>((normalizedHeight - 0.8f) * 5 * 255));
                green = std::max(0, 255 - static_cast<int>((normalizedHeight - 0.8f) * 5 * 255));
            }

            // Establecer el color
            SDL_SetRenderDrawColor(renderer, red, green, blue, 255);

            // Dibujar un bloque de terreno de mayor tamaño
            SDL_Rect rect = { x * blockSize, y * blockSize, blockSize, blockSize };
            SDL_RenderFillRect(renderer, &rect);
        }
    }
}

int main(int argc, char* argv[]) {
    // Comprobar si se pasaron argumentos
    float scale = 50.0f;  // Reducimos la escala para hacer las islas más densas

    if (argc > 1) {
        // Si se pasa un argumento, se utiliza como la escala
        scale = std::atof(argv[1]);
        std::cout << "Usando escala: " << scale << std::endl;
    }

    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;

    SDL_Init(SDL_INIT_VIDEO);
    window = SDL_CreateWindow("Generador de Islas con Ruido de Perlin", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    // Generación del terreno
    std::vector<std::vector<float>> terrain(WINDOW_HEIGHT / BLOCK_SIZE, std::vector<float>(WINDOW_WIDTH / BLOCK_SIZE, 0.0f));
    generateTerrain(terrain, WINDOW_WIDTH / BLOCK_SIZE, WINDOW_HEIGHT / BLOCK_SIZE, scale);  // Generar terreno usando ruido de Perlin

    bool running = true;
    SDL_Event event;

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT || (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE)) {
                // Cerrar el programa cuando se presiona "Escape"
                running = false;
            }
        }

        // Renderizar mapa
        SDL_RenderClear(renderer);
        renderMap(renderer, terrain, BLOCK_SIZE);
        SDL_RenderPresent(renderer);

        SDL_Delay(16); // Simular 60 FPS
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}