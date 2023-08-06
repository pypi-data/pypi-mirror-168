#ifndef __EXP_VARIABLE_H__
#define __EXP_VARIABLE_H__

#include <cmath>
#include <random>
#include <stdexcept>

/**
 * @brief Class that generates values on an exponential distribution.
 *
 * This class inherits from the RandomVariable class and is used to generate a
 * random number according to an exponential distribution. The object must be
 * created first, and the numbers can subsequently be obtained through class
 * methods. On the Simulator, this class is used to generate the arrival and
 * departure variable values.
 *
 */
class ExpVariable {
 public:
  /**
   * @brief Constructs a new Exponential Variable object. The parameters are set
   * by default according to the RandomVariable method from the Random Variable
   * class.
   *
   */
  ExpVariable(void);
  /**
   * @brief Constructs a new Exponential Variable object. This method is
   * inherited from the Random Variable class.
   *
   * @param seed the seed that is used as a source of randomness by a random
   * number engine to generate a new value inside the object.
   * @param parameter1 the parameter value. It must be a positive number.
   */
  ExpVariable(unsigned int seed, double parameter1);
  /**
   * @brief Generates a new value according to an exponential distribution
   * inside the ExpVariable object. Said object must have been previously
   * created.
   *
   *
   * @return double the new exponential variable value.
   */
  double getNextValue(void);

 private:
  std::uniform_real_distribution<double> dist;
  std::mt19937 generator;
  double parameter1;
};

#endif