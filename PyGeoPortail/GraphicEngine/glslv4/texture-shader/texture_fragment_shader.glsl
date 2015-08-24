/* *********************************************************************************************** */

// #shader_type fragment

#version 330

/* *********************************************************************************************** */

uniform sampler2D texture0;

/* *********************************************************************************************** */

in VertexAttributes
{
  vec2 uv;
} vertex;

/* *********************************************************************************************** */

out vec4 fragment_colour;

/* *********************************************************************************************** */

float
min3(vec3 rgb)
{
  return min(rgb.r, min(rgb.g, rgb.b));
}

float
max3(vec3 rgb)
{
  return max(rgb.r, max(rgb.g, rgb.b));
}

float
mean3(vec3 rgb)
{
  return (rgb.r + rgb.g + rgb.b) / 3.;
}

vec4
rgb_to_hsl(vec3 rgb)
{
  float min_rgb = min3(rgb);
  float max_rgb = max3(rgb);
  float chroma = max_rgb - min_rgb; // radius, small for grayscale

  float hue; // polar angle
  if (chroma == .0)
    hue = .0; // undefined
  else if (max_rgb == rgb.r)
    {
      hue = ((rgb.g - rgb.b) / chroma); // in [-1, 1]
      if (hue < 0)
	hue += 6.;
    }
  else if (max_rgb == rgb.g)
    hue = (rgb.b - rgb.r) / chroma + 2.; // in [1, 3]
  else if (max_rgb == rgb.b)
    hue = (rgb.r - rgb.g) / chroma + 4.; // in [3, 5]
  // hue *= 60.;
  hue /= 6.;

  float lightness = .5 * (max_rgb + min_rgb); // 0 means black and 1 means white

  float saturation;
  if (lightness == .0 || lightness == 1.)
    saturation = .0;
  else
    saturation = chroma / (1 - abs(max_rgb + min_rgb - 1));
  /*
  if (lightness < .5)
    saturation = chroma / (max_rgb + min_rgb);
  else if (lightness >= .5)
    saturation = chroma / (2. - (max_rgb + min_rgb))
  */

  // return normalised float
  return vec4(hue, saturation, lightness, chroma);
}

/* *********************************************************************************************** */

void 
hsl_filter(vec3 texel)
{
  vec4 hsv = rgb_to_hsl(texel);
  float h = hsv.x;
  float s = hsv.y;
  float l = hsv.z;
  float chroma = hsv.a;

  /* fragment_colour = vec4(h, s, l, 1.); */
  /* fragment_colour = vec4(h, chroma, l, 1.); */
  /* fragment_colour = vec4(h, h, h, 1.); */
  /* fragment_colour = vec4(s, s, s, 1.); */
  /* fragment_colour = vec4(l, l, l, 1.); */

  /* float level_line_inf = 5. / 360.; */
  /* float level_line_sup = 50. / 360.; */
  float level_line_inf = 70. / 360.;
  float level_line_sup = 180. / 360.;
  
  if (h >= level_line_inf && h <= level_line_sup
      && l > .25 && s > .10)
    fragment_colour = vec4(texel, 1);
  else
    fragment_colour = vec4(1);
}

/* *********************************************************************************************** */

void main()
{
  vec3 texel = texture(texture0, vertex.uv).rgb;
  
  fragment_colour = vec4(texel, 1.);

  // float g = min(texel.g, .6);
  // // fragment_colour = vec4(g, g, g, 1.);
  // // float l = 1 - max(max(texel.r, texel.g), texel.b);
  // float l = 1 - (texel.r + texel.g + texel.b)/3.;
  // // if (l < .1)
  // //   l = 1;
  // fragment_colour = vec4(l, l, l, 1.);
  
  // hsl_filter(texel);
  
  /* vec4 hsv = rgb_to_hsl(texel); */
  /* float h = hsv.x; */
  /* float s = hsv.y; */
  /* float l = hsv.z; */
  /* float chroma = hsv.a; */
  /* fragment_colour = vec4(h, s, l, 1.); */
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
