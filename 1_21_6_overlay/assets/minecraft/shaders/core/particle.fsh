#version 150

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;

out vec4 fragColor;

void main() {
    vec4 rgb = floor(texture(Sampler0, texCoord0) * 255);
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (rgb.r == 162 && rgb.g == 162 && rgb.b == 162 && rgb.a == 252) {
        color = texture(Sampler0, texCoord0);
    }
    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
}
