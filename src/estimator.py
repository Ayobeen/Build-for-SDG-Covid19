import math
import json
# Defining covid-19 constants..........
NORMAL_INFECTION_GROWTH_RATE = 10
SEVERE_INFECTION_GROWTH_RATE = 50
PERCENTAGE_POSITIVE_CASES = 0.15
PERCENTAGE_HOSPITAL_BED_AVAILABILITY = 0.35
PERCENTAGE_CASES_NEEDS_FOR_ICU_CARE = 0.05
PERCENTAGE_CASES_NEEDS_FOR_VENTILATION = 0.02

sampleCaseData = {}
responseJSON = {}
responseJSON['data'] = {}
responseJSON['impact'] = {}
responseJSON['severeImpact'] = {}


def calculateCurrentlyInfected():
    """ /**
   * @function calculateCurrentlyInfected
   * @param sampleCaseData
   * @returns currentlyInfected
   * @description estimates and saves  the number of currently and severly infected people
   */
   """
    global sampleCaseData, responseJSON
    # update impact

    saveCurrentlyInfected = (sampleCaseData['reportedCases'] * NORMAL_INFECTION_GROWTH_RATE)
    responseJSON['impact']['currentlyInfected'] = saveCurrentlyInfected
    # update severeImpact
    saveSeverelyInfected = (sampleCaseData['reportedCases'] * SEVERE_INFECTION_GROWTH_RATE)
    responseJSON['severeImpact']['currentlyInfected'] = saveSeverelyInfected


def calculateInfectionRatesPerPeriod(numberOfDays, periodType):
    """/**
   * @def calculateInfectionRatesPerPeriod
   * @params numberOfDays, periodType
   * @returns infectionRatioPerPeriod
   * @description normalise the duration input to days, and then do your computation based on periods in days, weeks and months.
   */
   """
    infectionRatioPerPeriod = 0
    if periodType == 'days':
        infectionRatioPerPeriod = pow(2, math.trunc(numberOfDays / 3))
    elif periodType == 'weeks':
        infectionRatioPerPeriod = pow(2, (math.trunc((numberOfDays * 7) / 3)))
    else:
        infectionRatioPerPeriod = pow(2, (numberOfDays * 10))

    return infectionRatioPerPeriod


def calculateIAndReturnPeriods(numberOfDays, periodType):
    """
    /**
   * @def calculateIAndReturnPeriods
   * @params numberOfDays, periodType
   * @returns infectionRatioPerPeriod
   * @description normalise the duration input based on periods in days, weeks and months.
   */
  """

    infectionRatioPerPeriod = 0
    if periodType == 'days':
        infectionRatioPerPeriod = numberOfDays
    elif periodType == 'weeks':
        infectionRatioPerPeriod = (math.trunc(numberOfDays * 7))
    else:
        infectionRatioPerPeriod = (math.trunc(numberOfDays * 30))

    return infectionRatioPerPeriod


def calculatePossibleInfectionGrowthRate():
    """
    /**
   * @def calculatePossibleInfectionGrowthRate
   * @param sampleCaseData
   * @returns infectionsByRequestedTime
   * @description To estimate the number of infected people 30 days from now,
   */
  """
    global sampleCaseData, responseJSON
    INFECTION_RATE_PER_PERIOD = calculateInfectionRatesPerPeriod(
        sampleCaseData['timeToElapse'], sampleCaseData['periodType'])
    # update impact
    saveNormalSpreadRate = responseJSON['impact']['currentlyInfected'] * \
        INFECTION_RATE_PER_PERIOD
    responseJSON['impact']['infectionsByRequestedTime'] = saveNormalSpreadRate
    # update severeImpact
    saveSevereSpreadRate = responseJSON['severeImpact']['currentlyInfected'] * \
        INFECTION_RATE_PER_PERIOD
    responseJSON['severeImpact']['infectionsByRequestedTime'] = saveSevereSpreadRate


def calculateSevereCases():
    """
    /**
   * @def calculateSevereCases
   * @param sampleCaseData
   * @returns severeCasesByRequestedTime
   * @description This is the estimated number of severe positive cases that will require hospitalization to recover.
   */
  """
    global sampleCaseData, responseJSON
    # update impact
    estimatedNormalPositive = responseJSON['impact']['infectionsByRequestedTime'] * \
        PERCENTAGE_POSITIVE_CASES
    responseJSON['impact']['severeCasesByRequestedTime'] = estimatedNormalPositive

    # update severeImpact
    estimatedSeverePositive = responseJSON['severeImpact']['infectionsByRequestedTime'] * \
        PERCENTAGE_POSITIVE_CASES
    responseJSON['severeImpact']['severeCasesByRequestedTime'] = estimatedSeverePositive


def caclulateHospitalBedsAvailability():
    """
    /**
   * @def caclulatHospitalBedsAvailability
   * @param sampleCaseData
   * @returns hospitalBedsByRequestedTime
   * @description This is the estimated a 35% bed availability in hospitals for severe COVID-19 positive patients.
   */
  """
    global sampleCaseData, responseJSON
    # update impact
    HOSPITAL_BEDS_AVAILABLE = sampleCaseData['totalHospitalBeds'] * \
        PERCENTAGE_HOSPITAL_BED_AVAILABILITY
    saveNormalHospitalBedAvailable = math.trunc(
        HOSPITAL_BEDS_AVAILABLE - responseJSON['impact']['severeCasesByRequestedTime'])
    responseJSON['impact']['hospitalBedsByRequestedTime'] = saveNormalHospitalBedAvailable
    # update severeImpact
    saveSevereHospitalBedAvailable = math.trunc(
        HOSPITAL_BEDS_AVAILABLE - responseJSON['severeImpact']['severeCasesByRequestedTime'])
    responseJSON['severeImpact']['hospitalBedsByRequestedTime'] = saveSevereHospitalBedAvailable


def calculationICURequirement():
    """
    /**
   * @def calculationICURequirement
   * @param sampleCaseData
   * @returns casesForICUByRequestedTime
   * @description This is the estimated number of severe positive cases that will require ICU care.
   */
   """
    global sampleCaseData, responseJSON
    # update impact
    saveNormalCasesNeadingICUCare = math.trunc(
        responseJSON['impact']['infectionsByRequestedTime'] * PERCENTAGE_CASES_NEEDS_FOR_ICU_CARE)
    responseJSON['impact']['casesForICUByRequestedTime'] = saveNormalCasesNeadingICUCare
    # update severeImpact
    saveSeverCasesNeadingICUCare = math.trunc(
        responseJSON['severeImpact']['infectionsByRequestedTime'] * PERCENTAGE_CASES_NEEDS_FOR_ICU_CARE)
    responseJSON['severeImpact']['casesForICUByRequestedTime'] = saveSeverCasesNeadingICUCare


def calculateVentilatorsRequired():
    """
    /**
   * @def calculateVentilatorsRequired
   * @param sampleCaseData
   * @returns casesForVentilatorsByRequestedTime
   * @description This is the estimated number of severe positive cases that will require ventilators
   */
  """
    global sampleCaseData, responseJSON
    # update impact
    saveNormalCasesNeedingVentilators = math.trunc(
        responseJSON['impact']['infectionsByRequestedTime'] * PERCENTAGE_CASES_NEEDS_FOR_VENTILATION)
    responseJSON['impact']['casesForVentilatorsByRequestedTime'] = saveNormalCasesNeedingVentilators
    # update severeImpact
    saveSeverCasesNeedingVentilators = math.trunc(
        responseJSON['severeImpact']['infectionsByRequestedTime'] * PERCENTAGE_CASES_NEEDS_FOR_VENTILATION)
    responseJSON['severeImpact']['casesForVentilatorsByRequestedTime'] = saveSeverCasesNeedingVentilators


def calculateCostImapctOnEconomy():
    """
  /**
   * @def calculateCostImapctOnEconomy
   * @param sampleCaseData
   * @returns dollarsInFlight
   * @description estimate how much money the economy is likely to lose over the said period.
   */
  """
    global sampleCaseData, responseJSON
    PERIOD_IN_FOCUS = calculateIAndReturnPeriods(
        sampleCaseData['timeToElapse'], sampleCaseData['periodType'])
    MAJORITIY_WORKING_POPULATION = sampleCaseData['region']['avgDailyIncomePopulation']
    DAILY_EARNINGS = sampleCaseData['region']['avgDailyIncomeInUSD']

    # update impact
    saveNormalDollarsInFlight = math.trunc(
        (responseJSON['impact']['infectionsByRequestedTime'] * MAJORITIY_WORKING_POPULATION * DAILY_EARNINGS) / PERIOD_IN_FOCUS)
    responseJSON['impact']['dollarsInFlight'] = saveNormalDollarsInFlight
    # update severeImpact
    saveSeverDollarInFlight = math.trunc(
        (responseJSON['severeImpact']['infectionsByRequestedTime'] * MAJORITIY_WORKING_POPULATION * DAILY_EARNINGS) / PERIOD_IN_FOCUS)
    responseJSON['severeImpact']['dollarsInFlight'] = saveSeverDollarInFlight


def initCovidEstimator(data):
  """ /**
 * @function initCovidEstimator
 * @param data
 * @returns Array
 * @description application Entry point.
 */
 """
  global sampleCaseData, responseJSON
  # initialize variables
  # print('data')
  # print(data)
  # arrayToObjConvertion = dict.fromkeys(data)
  #arrayToObjConvertion = json.dumps(data)
  sampleCaseData = data
  responseJSON['data'] = data
  #print('konfa', responseJSON)
  # compute code challenge -1
  calculateCurrentlyInfected()
  calculatePossibleInfectionGrowthRate()

  # compute code challenge -2
  calculateSevereCases()
  caclulateHospitalBedsAvailability()

  # compute code challenge -3
  calculationICURequirement()
  calculateVentilatorsRequired()
  calculateCostImapctOnEconomy()

    # return responses
    #newRes = object_to_array(responseJSON)
  return  responseJSON
  
 

def estimator(data):
    return initCovidEstimator(data)
