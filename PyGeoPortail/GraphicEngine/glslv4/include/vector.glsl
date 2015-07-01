/* *********************************************************************************************** *
 *
 * Vector Fucntion
 *
 *
 *   Nomenclature:
 *     pi point
 *     vi vector
 *     ui assume an unit vector
 * 
/* *********************************************************************************************** */

/* *********************************************************************************************** *
 *
 * 
 *
 */

float
cross(in vec2 v1, in vec2 v2)
{
  return v1.x*v2.y - v1.y*v2.x;
}

float
cos_between(in vec2 u1, in vec2 u2)
{
  return dot(u1, u2);
}

float
sin_between(in vec2 u1, in vec2 u2)
{
  return cross(u1, u2);
}

float
tan_between(in vec2 v1, in vec2 v2)
{
  // cos = A.B / |A||B|
  // sin = AxB / |A||B|
  // tan = sin / cos = AxB / A.B
  return cross(v1, v2) / dot(v1, v2);
}

float
angle_between(in vec2 v1, in vec2 v2)
{
  return atan(tan_between(v1, v2));
}

/* *********************************************************************************************** *
 *
 * Composition
 *
 */

vec2
middle(in vec2 p1, in vec2 p2)
{
  return .5 * (p1 + p2);
}

vec2
direction(in vec2 p1, in vec2 p2)
{
  return normalize(p2 - p1);
}
  
/* *********************************************************************************************** *
 *
 * Symmetry
 *
 */

vec2
parity(in vec2 v)
{
  return -v;
}

vec2
mirror_x(in vec2 v)
{
  return vec2(-v.x, v.y);
}

vec2
mirror_y(in vec2 v)
{
  return vec2(v.x, -v.y);
}

/* *********************************************************************************************** *
 *
 * Rotation
 *
 */

vec2
normal(in vec2 v)
{
  return vec2(-v.y, v.x);
}

vec2
rotate90(in vec2 v)
{
  return normal(v);
}

vec2
anti_rotate90(in vec2 v)
{
  return vec2(v.y, -v.x);
}

vec2
rotate(in vec2 v, in float angle)
{
  float c = cos(angle);
  float s = sin(angle);
  return vec2(c*v.x - s*v.y,
	      s*v.x + c*v.y);
}

/* *********************************************************************************************** *
 *
 * Distance
 *
 */

// Returns distance of p3 to line passing by p1 and p2
float
signed_distance(in vec2 p1, in vec2 p2, in vec2 p3)
{
  vec2 v21 = p2 - p1;
  vec2 v31 = p3 - p1;
  return cross(v21, v31) / length(v21);
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
