#version 460 core

const vec2 GRID_DIMS = vec2(50, 50);
const vec4 COL_WHITE = vec4(1.0, 1.0, 1.0, 1.0);
const vec4 COL_ODD = vec4(0.0, 0.0, 0.0, 1.0);
const vec4 COL_RED = vec4(1.0, 0.0, 0.0, 1.0);
const vec4 COL_GREEN = vec4(0.0, 1.0, 0.0, 1.0);
const vec4 COL_BLUE = vec4(0.0, 0.0, 1.0, 1.0);

layout(std430, binding = 1) buffer automatonLayout
{
    int width;
    int height;
    int cell_width;
    int cell_height;
    int map[];
};

in vec2 fragpos;
out vec4 fragColor;

void main()
{
    vec2 dims = vec2(width, height);
    vec2 slot = fragpos * vec2(1280.0, 720) / vec2(float(cell_width), float(cell_height));
    int x = int(slot.x);
    int y = int(slot.y);

    if(x < dims.x && y < dims.y){
        if(map[y * width + x] == 1)
            fragColor = COL_WHITE;
    }
}
