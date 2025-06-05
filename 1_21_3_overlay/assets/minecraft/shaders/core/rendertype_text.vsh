#version 150

#moj_import <minecraft:fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;
uniform vec2 ScreenSize;
uniform mat3 IViewRotMat;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;

flat out int p;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    vertexDistance = 1.0;
    vertexColor = Color * texelFetch(Sampler2, UV2 / 16, 0);
    texCoord0 = UV0;

    const vec2[4] corners = vec2[4](vec2(0), vec2(0, 1), vec2(1), vec2(1, 0));
    vec2 coord = corners[gl_VertexID % 4];

    float alpha = round(texture(Sampler0, UV0).a * 255);

    p = 0;
    if (alpha == 251 && Position.z > 0)
    {   
        p = 1;
        gl_Position.xy = vec2(coord * 2 - 1) * vec2(1, -1);
        gl_Position.zw = vec2(-1, 1);
        vertexColor = Color;
    }
}
