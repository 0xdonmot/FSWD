require('dotenv').config()

const AUTH0_DOMAIN = process.env.AUTH0_DOMAIN
const API_SERVER_URL = process.env.API_SERVER_URL
const API_AUDIENCE = process.env.API_AUDIENCE
const CLIENT_ID = process.env.CLIENT_ID
const CALLBACK_URL = process.env.CALLBACK_URL

export { AUTH0_DOMAIN, API_SERVER_URL, API_AUDIENCE, CLIENT_ID, CALLBACK_URL }

