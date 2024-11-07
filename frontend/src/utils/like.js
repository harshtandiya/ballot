import { createResource } from 'frappe-ui'

export const toggleLike = (
  reference_doctype,
  reference_name,
  comment_email,
) => {
  return createResource({
    url: 'ballot.api.like.toggle_like',
    makeParams() {
      return {
        reference_doctype: reference_doctype,
        reference_name: reference_name,
        comment_email: comment_email,
      }
    },
    onSuccess() {
      return [1, 'Liked Successfully']
    },
    onError(err) {
      return [0, err.messages]
    },
  })
}

export const checkAlreadyLiked = (
  reference_doctype,
  reference_name,
  comment_email,
) => {
  return createResource({
    url: 'ballot.api.like.is_already_liked',
    makeParams() {
      return {
        comment_email: comment_email,
        reference_doctype: reference_doctype,
        reference_name: reference_name,
      }
    },
    auto: true,
  })
}

export const getLikeCount = (reference_doctype, reference_name) => {
  return createResource({
    url: 'ballot.api.like.get_likes_count',
    makeParams() {
      return {
        reference_doctype: reference_doctype,
        reference_name: reference_name,
      }
    },
    auto: true,
  })
}
