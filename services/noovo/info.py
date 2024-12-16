
import json
import requests

import common


class Info:

    def Shows(self, show: common.Show) -> None:
        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graph_operation_name = "axisMedia"

        graphql_variables: dict[str, str | list[str]] = {
		    "authenticationState": "UNAUTH",
		    "axisMediaId": "contentid/axis-media-50652",
		    "language": "FRENCH",
		    "maturity": "ADULT",
		    "playbackLanguage": "FRENCH",
		    "subscriptions": [
		    	"CANAL_D",
		    	"CANAL_VIE",
		    	"INVESTIGATION",
		    	"NOOVO",
		    	"Z"
		    ]
        }

        graphql_query = """
query axisMedia($axisMediaId: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {
  contentData: axisMedia(id: $axisMediaId) {
    description
    agvotCode
    qfrCode
    originalSpokenLanguage
    genres {
      name
    }
    heroBrandLogoId
    adUnit {
      ...AxisAdUnitData
    }
    mainContents {
      ...MainContentsData
    }
    cast {
      role
      castMembers {
        fullName
      }
    }
    normalizedRatingCodes {
      language
      ratingCodes
    }
    originNetworkUrl
    mediaType
    firstAirYear
    seasons {
      title
      id
      seasonNumber
      metadataUpgrade {
        userIsSubscribed
        packageName
        languages
        userIsSubscribed
      }
    }
  }
}

fragment AxisAdUnitData on AxisAdUnit {
  adultAudience
  heroBrand
  pageType
  product
  revShare
  title
  analyticsTitle
  keyValue {
    webformType
    adTarget
    contentType
    mediaType
    pageTitle
    revShare
    subType
  }
}

fragment AuthConstraintsData on AuthConstraint {
  authRequired
  packageName
  endDate
  language
  startDate
  subscriptionName
  
}

fragment MainContentsData on Collection {
  page {
    items {
      id
      title
      ... on AxisContent {
        axisId
        previewMode
        path
        seasonNumber
        episodeNumber
        summary
        duration
        availablePlaybackLanguages
        languageMeta {
          language
          playbackIndicators
          
        }
        playbackMetadata {
          indicator
          languages {
            languageCode
            languageDisplayName
            
          }
          
        }
        authConstraints {
          ...AuthConstraintsData
          
        }
        featureImages: images(formats: THUMBNAIL) {
          url
          
        }
        
        badges {
          title
          label
          
        }
      }
      
    }
    
  }
  
}
"""
        data: dict[str, str | dict[str, str | list[str]]] = {
            "operationName": graph_operation_name,
            "query": graphql_query,
            "variables": graphql_variables,
        }

        headers = {
            "content-type": "application/json"
        }

        r = requests.post(url, headers=headers, data=json.dumps(data))

        try:
            resp = r.json()
            with open("wow.json", "wt") as f:
                f.write(json.dumps(resp))
            print(resp)
        except:
            print("FUCK")
        
        print("WAIT")
