import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import { Amplify } from 'aws-amplify'
import amplify_outputs from '../amplify_outputs/amplify_outputs.json'
import './index.css'
import App from './App.jsx'
import { initOutboundLinkTracking } from './utils/analytics.js'

// Force explicit regions for Auth and GraphQL to avoid environment region drift
const config = {
  ...amplify_outputs,
  Auth: {
    Cognito: {
      identityPoolId: amplify_outputs.auth?.identity_pool_id,
      identityPoolRegion: amplify_outputs.auth?.aws_region,
      userPoolId: amplify_outputs.auth?.user_pool_id,
      userPoolClientId: amplify_outputs.auth?.user_pool_client_id,
      loginWith: { email: true },
    },
  },
  API: {
    GraphQL: {
      endpoint: amplify_outputs.data?.url,
      region: amplify_outputs.data?.aws_region,
      defaultAuthMode:
        amplify_outputs.data?.default_authorization_type === 'AWS_IAM'
          ? 'iam'
          : 'userPool',
    },
  },
}

Amplify.configure(config)

// Initialize outbound link tracking for GA4
initOutboundLinkTracking()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <HashRouter>
      <App />
    </HashRouter>
  </StrictMode>,
)
