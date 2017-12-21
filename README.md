# sgizmo

This package was created to easily download objects from the SurveyGizmo API (version 5). It supports changing the domain for users outside the US (e.g., 'restapica' for Canadian users, instead of 'restapi').

Uploading objects is not currently supported, but the **make_url** function can be easily adapted to work with POST and UPDATE api requests.

### Installing

```
    pip install sgizmo
```

## Getting Started
SurveyGizmo's API has 3 domains:
* 'restapi' (US users/account holders)
* 'restapica' (Canadian users/account holders)
* 'restapieu' (EU users/account holders)  

API calls will return an authentication error if you are using the incorrect domain (i.e., a domain different from the one in which your user account is registered). The domain can be changed by passing one of the strings above as the domain parameter in any of the get functions. The default domain is US ('restapi').

**Your API token should be in the format: 'api_token=[x]&api_token_secret=[y]'**

Available functions:
```
    get_survey_list(api_token)
    
    get_survey(api_token, survey_id)
    
    get_questions(api_token, survey_id)
    
    get_question_option(api_token, survey_id, question_id)
    
    get_all_survey_options(api_token, survey_id)
    
    get_survey_responses(api_token, survey_id)
    
    get_contact_lists(api_token)
    
    get_contact_list(api_token, list_id)
    
    get_contacts(api_token, contact_list_id)
    
    get_contact(api_token, contact_list_id, contact_id)
    
    get_campaigns(api_token, survey_id)
    
    get_campaign(api_token, survey_id, campaign_id)
    
    get_campaign_emails(api_token, survey_id, campaign_id)
    
    get_campaign_email(api_token, survey_id, campaign_id, email_id)
    
    make_url(...)
```

The function get_all_survey_options makes repeated calls to the SurveyGizmo API, so pass a non-zero value to the wait_sec parameter to avoid exceeding your API call rate limits when downloading large numbers of options.

## Authors

**Garret Cree** - [GCCree](https://github.com/GCCree)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

Mussie for all his wisdom and guidance over the development of this package ([muchichi](https://github.com/muchichi))
