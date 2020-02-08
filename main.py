import requests
import json
from pprint import pprint

baseUrl = 'https://apiw.westjet.com/bookingservices'
defaultTime = '2020-12-09T07:30:00'
defaultSource = 'YYC'
defaultDestination = 'SEA'
defaultFlightNumber = '7890'

def getSeatMapUrl():
    return baseUrl + '/seatmap/extendedSeatmap'

def getParams(time, source, destination, flightNumber):
    return {'segment': 1,
              'flightInfo': json.dumps([
                  {"flight":[
                      {"fareClass": "K",
                       "flightNumber": flightNumber,
                       "airlineCodeMarketing": "WS",
                       "departureDateTime": time,
                       "arrivalDateTime": time, # this value is ignored as long as format is correct so no need to fetch
                       "arrival": destination,
                       "departure": source
                       }
                  ]}
              ]),
              'pointOfSale': 'QkFC',
              'hasInfant': False,
              'bookId': 'a-random-key',
              'passengerInfo': json.dumps([
                  {"passengerTitle": "MR",
                   "dateOfBirth": "2000-01-01",
                   "firstName": "Godian",
                   "middleName": "",
                   "lastName": "test",
                   "ageOfMajority": False,
                   "gender": "Male",
                   "loyaltyProgramName": "",
                   "loyaltyProgramMemberId": "",
                   "type": "adult",
                   "displayIndex": 0,
                   "perks": []
                   }
              ])
            }

def getSeatsDetails():
    time = input("Enter Departure time [{}]: ".format(defaultTime)) or defaultTime
    source = input("Enter source airport code [{}]: ".format(defaultSource)) or defaultSource
    destination = input("Enter destination airport code [{}]: ".format(defaultDestination)) or defaultDestination
    flightNumber = input("Enter flight number [{}]: ".format(defaultFlightNumber)) or defaultFlightNumber

    response = requests.get(getSeatMapUrl(), params=getParams(time, source, destination, flightNumber))

    if response.status_code == 200:
        jsonRes = json.loads(response.content)
        rows = jsonRes['aircraft']['deck']['cabin']['rows']
        results = []
        for row in rows:
            for seat in row['seats']:
                result = []
                result.append(seat['seatNumber'])
                occupied = seat['occupied']
                result.append('Availble' if not occupied else 'Not available')
                result.append(seat['prices'][0]['price'] if not occupied else 'NA')
                results.append(result)
        pprint(results)
    else:
        pprint('Received {} error {}'.format(response.status_code, response.content))

if __name__ == '__main__':
    getSeatsDetails()
