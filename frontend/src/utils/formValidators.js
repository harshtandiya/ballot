export function getFieldErrors(field) {
  const fieldErrors = []

  // Check if field has a label
  if (
    !field.label &&
    field.fieldtype != 'Section Break' &&
    field.fieldtype != 'Column Break'
  ) {
    fieldErrors.push(
      `Field "${field.fieldname || 'unknown'}" is missing a label.`,
    )
  }

  // Check if field has a fieldname
  if (!field.fieldname) {
    fieldErrors.push(
      `Field "${field.label || 'unknown'}" is missing a field name.`,
    )
  }

  // Check if field is a select type and has options
  if (
    field.fieldtype === 'Select' &&
    (!field.options || field.options.length === 0)
  ) {
    fieldErrors.push(
      `Field "${field.label}" (fieldname: ${field.fieldname}) is a select type but has no options.`,
    )
  }

  return fieldErrors
}
