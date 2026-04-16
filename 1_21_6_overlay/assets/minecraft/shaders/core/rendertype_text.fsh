#version 150

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:globals.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;

flat in int p;

out vec4 fragColor;

void main() {
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;

    vec3 rgb = vec3(floor(color.r * 255), floor(color.g * 255), floor(color.b * 255));
    if (rgb.r == 126 && rgb.g == 252 && rgb.b == 31) {
        color = texture(Sampler0, texCoord0) * vec4(1.0, 0.0, 0.0, 1) * ColorModulator;
    }

    if (p == 1)
    {
        color = vec4(0, 0, 0, 1);
        vec2 centerUV = gl_FragCoord.xy / ScreenSize - 0.5;
        
        if (abs(centerUV.y) * 2 < 1 - mix(vertexColor.r, vertexColor.b, vertexColor.a))
        {
            color = vec4(0);
        }
        //color = vec4(ScreenSize.x * 255123, ScreenSize.x, ScreenSize.x, 1);
    }

    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
}
