import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import isToday from 'dayjs/plugin/isToday'
import isYesterday from 'dayjs/plugin/isYesterday'

dayjs.extend(relativeTime)
dayjs.extend(isToday)
dayjs.extend(isYesterday)

export const getRedirectUrl = (route) => {
  return window.location.origin + '/' + route
}

export const generateRandomId = () => {
  return Math.random().toString(36).slice(2, 8)
}

export const getRelativeTime = (datetime) => {
  const date = dayjs(datetime)
  if (date.isToday()) {
    return 'Today'
  } else if (date.isYesterday()) {
    return 'Yesterday'
  } else {
    return date.fromNow()
  }
}
