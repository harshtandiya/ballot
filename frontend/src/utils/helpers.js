export const getRedirectUrl = (route) => {
  return window.location.origin + '/' + route
}

export const generateRandomId = () => {
  return Math.random().toString(36).slice(2, 8)
}
