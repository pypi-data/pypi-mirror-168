#ifndef __UNIFORM_VARIABLE_H__
#define __UNIFORM_VARIABLE_H__

#include <random>
#include <stdexcept>

/**
 * @brief Class that generates values on an uniform distribution.
 *
 * This class inherits from the RandomVariable class and is used to generate a
 * random number with an uniform distribution on an interval. This interval can
 * either be specified or set by default. The object must be created first, and
 * the values can subsequently be obtained through class methods. On the
 * Simulator, this class is used to generate the source, destination and
 * bitRate variable values.
 *
 */
class UniformVariable {
 public:
  /**
   * @brief Constructs a new Uniform Variable object.
   *
   * @param seed the seed that is used as a source of randomness by a random
   * number engine to generate a new value inside the object.
   * @param parameter1 the upper bound of the uniform distribution interval. It
   * must be a positive number.
   */
  UniformVariable(unsigned int seed, double parameter1);
  /**
   * @brief Generates a new value according to an uniform distribution on the
   * established interval of the UniformVariable object. Said object must have
   * been previously created.
   *
   * @return double the new uniform variable value.
   */
  double getNextValue(void);
  /**
   * @brief Generates a new value according to an uniform distribution on the
   * established interval of the UniformVariable object. Said object must have
   * been previously created.
   *
   * @return double the new uniform variable value.
   */
  double getNextIntValue(void);

 private:
  std::uniform_int_distribution<int> dist;
  std::mt19937 generator;
  double parameter1;
};

#endif