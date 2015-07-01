/* *********************************************************************************************** */

// #shader_type fragment

#version 330

/* *********************************************************************************************** */

/* 
 * The filter diameter can be larger than a pixel. In fact, according to the Sampling Theorem
 * (f_sampling >= 2 * f_max), it should be greater than a pixel to perform proper antialiasing. On
 * the other hand, if we make the filter size too large, then the lines will become excessively
 * blurry.
 */
uniform float antialias_diameter = 1;

/* *********************************************************************************************** */

in VertexAttributes
{
  vec2 uv;
  float line_length;
  float line_width;
  vec4 colour;
  float cap;
} vertex;

/* *********************************************************************************************** */

out vec4 fragment_colour;

/* *********************************************************************************************** */

// Compute distance to cap 
float
round_cap(float dx, float dy)
{
  return length(vec2(dx, dy));
}

/* *********************************************************************************************** */

void main()
{
  vec4 colour = vertex.colour;
  // If colour is fully transparent we just discard the fragment
  if (colour.a <= 0)
    discard;
  
  float u = vertex.uv.x;
  float v = vertex.uv.y;
  float t = vertex.line_width/2 - antialias_diameter; // Fixme: why - antialias_diameter ?

  float dy = abs(v);
  
  float line_stop = vertex.line_length;
  
  float d = 0;
  // start cap
  if (vertex.cap == -1) { // && u < .0
    d = round_cap(abs(u), dy);
  }
  // stop cap
  else if (vertex.cap == 1 && u > line_stop)
    d = round_cap(u - line_stop, dy);
  else
    d = dy;
  
  // Anti-alias test, distance to border
  d -= t;
  if (d < 0)
    fragment_colour = colour;
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
