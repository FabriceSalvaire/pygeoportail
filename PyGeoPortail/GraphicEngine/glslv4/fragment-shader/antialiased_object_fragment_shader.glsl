/* *********************************************************************************************** */

// #shader_type fragment

#version 330

/* *********************************************************************************************** */

uniform float antialias_diameter = 1;

/* *********************************************************************************************** */

in VertexAttributes
{
  vec2 uv;
  float line_width;
  vec4 colour;
} vertex;

/* *********************************************************************************************** */

out vec4 fragment_colour;

/* *********************************************************************************************** */

void main()
{
  vec4 colour = vertex.colour;
  // If colour is fully transparent we just discard the fragment
  if (colour.a <= 0)
    discard;
  
  float u = vertex.uv.x;
  float v = vertex.uv.y;
  float t = vertex.line_width/2 - antialias_diameter;

  float du = abs(abs(u) - 1);
  float dy = abs(abs(v) - 1);
  float d = min(du, dy);
  
  // Anti-alias test, distance to border
  d -= t;
  if (d < 0)
    // fragment_colour = colour;
    fragment_colour = vec4(1);
  else
    {
      d /= antialias_diameter;
      fragment_colour = vec4(colour.xyz, exp(-d*d) * colour.a);
    }
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
