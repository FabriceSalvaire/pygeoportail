/* *********************************************************************************************** */

// #shader_type fragment

#version 330

/* *********************************************************************************************** */

uniform int cap_type = 1;
uniform int line_join = 1;
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
cap(int type, float dx, float dy, float t)
{
  return length(vec2(dx, dy));
}

// Compute distance to join
float
join(in vec2 uv, in float line_stop, in float line_width)
{
  float u = uv.x;
  float d = abs(uv.y);
  
  if (u < 0)
    d = max(d, length(uv));
  else if (u > line_stop)
    d = max(d, length(uv - vec2(line_stop, 0)));
  
  return d;
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
  float t = vertex.line_width/2 - antialias_diameter;

  float dy = abs(v);
  
  float line_start = 0;
  float line_stop = vertex.line_length;
  
  float d = 0;
  // start cap
  if (vertex.cap == -1) { //  && u < .0
    d = cap(cap_type, abs(u), dy, t);
    colour = vec4(1, 0, 0, 1); 
  }
  // stop cap
  else if (vertex.cap == 1 && u > line_stop)
    d = cap(cap_type, abs(u) - line_stop, dy, t);
  else
    d = join(vertex.uv, line_stop, vertex.line_width);
  
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
