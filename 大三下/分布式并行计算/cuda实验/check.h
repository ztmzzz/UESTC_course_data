#include <stdio.h>
#include <math.h>

void checkAccuracy(float *p, int nBodies)
{
  if (nBodies != 2<<11) return;

  // Assuming N is set to 11, the x y and z coordinates of a particle
  // (chosen at random) should
  // equal the following values:

  // -11.943975
  // 3.198896
  // 10.517184

  int position1IsCorrect  = ( (int)(p[9*6]) ) == -11;
  int position2IsCorrect  = ( (int)(p[(9*6) + 1] ) == 3);
  int position3IsCorrect  = ( (int)(p[(9*6) + 2] ) == 10);
  int positionsAreCorrect = (position1IsCorrect == 1) && (position2IsCorrect == 1) && (position3IsCorrect == 1);

  printf("%s\n", positionsAreCorrect
      ? "Simulator is calculating positions correctly."
      : "Simulator is not calculating positions correctly.");

  return;
}