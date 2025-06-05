#version 150

#moj_import <light.glsl>
#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in vec2 UV1;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;
uniform mat3 IViewRotMat;

uniform vec3 Light0_Direction;
uniform vec3 Light1_Direction;
uniform sampler2D Sampler0;

out float vertexDistance;
out vec4 vertexColor;
out vec4 lightColor;
out vec4 faceLightColor;
out vec2 texCoord0;
out vec2 texCoord1;
out vec2 texCoord2;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    vec4 finalColor = Color;
    texCoord0 = UV0;
    texCoord1 = UV1;
    texCoord2 = UV2;

    float r = floor(Color.r * 255);
    float g = floor(Color.g * 255);
    float b = floor(Color.b * 255);

    if (b == 0) {
        finalColor = vec4(1, 1, 1, 1);
        texCoord0.x += r * (16.0 / textureSize(Sampler0, 0).x);
        texCoord0.y += g * (16.0 / textureSize(Sampler0, 0).y);
    }

    vertexDistance = 1.0;
    vertexColor = finalColor;
    lightColor = minecraft_sample_lightmap(Sampler2, UV2);
    faceLightColor = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, vec4(1.0));
}
