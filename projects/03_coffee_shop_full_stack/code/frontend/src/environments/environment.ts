import { AUTH0_DOMAIN, API_SERVER_URL, API_AUDIENCE, CLIENT_ID, CALLBACK_URL } from './settings';

export const environment = {
  production: false,
  apiServerUrl: API_SERVER_URL, // the running FLASK api server url
  auth0: {
    url: AUTH0_DOMAIN, // the auth0 domain prefix
    audience: API_AUDIENCE, // the audience set for the auth0 app
    clientId: CLIENT_ID, // the client id generated for the auth0 app
    callbackURL: CALLBACK_URL, // the base url of the running ionic application. 
  }
};
