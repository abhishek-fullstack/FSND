/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', 
  auth0: {
    url: 'coffeeshopabhi.us', // the auth0 domain prefix
    audience: 'Coffee', // the audience set for the auth0 app
    clientId: 'cu456p8WXvSMoigW1c583FXFsigPdH4l', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
