#version 150

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:globals.glsl>

// by Falanta Fantomo

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec3 pos;

out vec4 fragColor;

float hash3D(vec3 p) {
    p = fract(p * vec3(123.34, 456.21, 789.13));
    p += dot(p, p + 45.32);
    return fract(p.x * p.y * p.z);
}

float noise3D(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);

    vec3 u = f * f * (3.0 - 2.0 * f);

    float a = hash3D(i);
    float b = hash3D(i + vec3(1.0, 0.0, 0.0));
    float c = hash3D(i + vec3(0.0, 1.0, 0.0));
    float d = hash3D(i + vec3(1.0, 1.0, 0.0));
    float e = hash3D(i + vec3(0.0, 0.0, 1.0));
    float f_edge = hash3D(i + vec3(1.0, 0.0, 1.0));
    float g = hash3D(i + vec3(0.0, 1.0, 1.0));
    float h = hash3D(i + vec3(1.0, 1.0, 1.0));

    return mix(
        mix(mix(a, b, u.x), mix(c, d, u.x), u.y),
        mix(mix(e, f_edge, u.x), mix(g, h, u.x), u.y),
        u.z
    );
}

float fbm3D(vec3 p) {
    float value = 0.0;
    float amplitude = 0.3;
    float frequency = 0.9;

    int levels = 10; // <=======

    for (int i = 0; i < levels; i++) {
        value += amplitude * noise3D(p * frequency);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

void main() {
    float max_modulator = max(ColorModulator.r, max(ColorModulator.g, ColorModulator.b));
    float t = smoothstep(0.15, 0.0, max_modulator);

    vec3 P1  = vec3(192.0, 216.0, 255.0) / 255.0;
    vec3 P2  = vec3(11.0, 12.0, 22.0) / 255.0;
    vec3 P1_ = vec3(47.0, 53.0, 76.0) / 255.0;
    vec3 P2_ = vec3(2.0, 2.0, 6.0) / 255.0;
    vec3 A_clear = vec3(mix(P1, P2, t));
    vec3 A_storm = vec3(mix(P1_, P2_, t));
    vec3 target_vector = A_storm - A_clear;
    vec3 current_vector = vec3(FogColor) - A_clear;
    float w = 0.0;
    float len_sq = dot(target_vector, target_vector);
    if (len_sq > 0.0001) {
        w = clamp(dot(current_vector, target_vector) / len_sq, 0.0, 1.0);
    }

    vec3 base_color = vec3(ColorModulator);
    vec3 cloud_color = vec3(1.0,1.0,1.0)*(((ColorModulator.r + ColorModulator.g + ColorModulator.b) / 3.0)+0.4-0.3*clamp(t+w,0.0,1.0));

    float mosaic_scale = 16.0;

    vec3 tiled_pos = floor(pos * mosaic_scale) / mosaic_scale;
    vec3 sky_coords_3d = vec3(tiled_pos.x * 0.05, GameTime * 20.0, tiled_pos.z * 0.05);

    sky_coords_3d.xz += GameTime * 20.0;

    float noise_density = fbm3D(sky_coords_3d);
    float cloud_factor = smoothstep(0.3, 0.8, clamp(noise_density+w*0.25,0.0,1.0));
    vec3 final_color = mix(base_color, cloud_color, cloud_factor);

    float effect_value = (16.0+8.0*clamp(t+w,0.0,1.0)) * 6;
    vec3 color_scaled = final_color * effect_value;
    vec3 base_step = floor(color_scaled);
    vec3 fraction = fract(color_scaled);

    vec2 grid = floor(pos.xz * mosaic_scale);
    float checker = mod(grid.x + grid.y, 2.0);

    vec3 dithered_step;
    for(int i = 0; i < 3; i++) {
        if (fraction[i] > 0.35 && fraction[i] < 0.65) {
            dithered_step[i] = base_step[i];
        } else {
            dithered_step[i] = floor(color_scaled[i] + 0.5);
        }
    }

    fragColor = apply_fog(vec4(dithered_step / effect_value, 1.0), sphericalVertexDistance, cylindricalVertexDistance, 0.0, FogSkyEnd, FogSkyEnd, FogSkyEnd, FogColor);
}
