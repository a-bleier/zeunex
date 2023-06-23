#version 460 core
layout (location = 0) in vec3 aPos;

out vec2 fragpos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
    fragpos = vec2(0.5)*gl_Position.xy + vec2(0.5);
    fragpos.y = 1.0 - fragpos.y;
}
