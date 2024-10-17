import { reactive } from 'vue'
import { generateRandomId } from './helpers'

export function getFieldTypes() {
  return [
    'Data',
    'Select',
    'Number',
    'Editor',
    'Textarea',
    'Section Break',
    'Column Break',
  ]
}

export function getStarterTemplate() {
  const fields = []
  fields.push(getStandardFields('Section Break'))
  fields.push(getStandardFields('Column Break'))
  fields.push(getStandardFields())
  return fields
}

export function getTemplateField() {
  return reactive({
    data: getStandardFields(),
    section_break: getStarterTemplate(),
    column_break: getStandardFields('Column Break'),
    number: getStandardFields('Number'),
    checkbox: getStandardFields('Checkbox'),
    editor: getStandardFields('Text Editor'),
    textarea: getStandardFields('Textarea'),
    select: getStandardFields('Select'),
  })
}

export function getStandardFields(
  fieldtype = 'Data',
  fieldname = '',
  label = '',
  value = '',
) {
  let _fieldname = ''
  if (!fieldname) {
    _fieldname = `${fieldtype.toLowerCase().split(' ').join('_')}_${generateRandomId()}`
  } else {
    _fieldname = fieldname
  }

  return {
    fieldtype: fieldtype,
    fieldname: _fieldname,
    label: label,
    value: value,
    mandatory: 0,
    options: '',
  }
}

export function addSectionBelow(fields, section) {
  const newSection = getStandardFields('Section Break') // New Section Break with the specified section name

  // Find the index of the specified section
  const index = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (index !== -1) {
    // Insert the new section break after the last field of the current section
    let insertIndex = index + 1

    // Iterate to find the end of the current section
    while (
      insertIndex < fields.value.length &&
      fields.value[insertIndex].fieldtype !== 'Section Break'
    ) {
      insertIndex++
    }

    // Insert the new section below the existing fields
    fields.value.splice(insertIndex, 0, newSection)
  }
}

export function addColumn(fields, section) {
  const newColumn = getStandardFields('Column Break')

  // Find the index of the section
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (sectionIndex !== -1) {
    // Find the position to insert the new column
    let insertIndex = sectionIndex + 1

    // Iterate over the fields starting from the section index to find the end of the current section
    for (let i = sectionIndex + 1; i < fields.value.length; i++) {
      if (fields.value[i].fieldtype === 'Section Break') {
        break
      }
      insertIndex = i + 1
    }

    // Insert the new column at the calculated position
    fields.value.splice(insertIndex, 0, newColumn)
  }
}

export function addField(fields, section, column, fieldtype) {
  const newField = getStandardFields(fieldtype)

  // Find the section index
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  // If the section is found
  if (sectionIndex !== -1) {
    // Find the position to insert the new field
    let insertIndex = fields.value.length // Default to end of fields

    // Iterate over the fields starting from the section index to find the correct insertion point
    for (let i = sectionIndex + 1; i < fields.value.length; i++) {
      // Check for the next section break
      if (fields.value[i].fieldtype === 'Section Break') {
        break
      }

      // Check for the column break within the section
      if (fields.value[i].fieldtype === 'Column Break') {
        if (fields.value[i].fieldname === column) {
          insertIndex = i + 1
        } else if (insertIndex === fields.value.length) {
          // If the current column is different and insertIndex has not been set, we should stop
          break
        }
      }

      // Update insertIndex to be right after the last field in the specified column
      if (
        fields.value[i].fieldtype !== 'Column Break' &&
        insertIndex !== fields.value.length
      ) {
        insertIndex = i + 1
      }
    }

    // Insert the new field at the calculated position
    fields.value.splice(insertIndex, 0, newField)
  }
}

// Reusable method to delete a specific field by its fieldname
export function deleteField(fields, fieldname) {
  const index = fields.value.findIndex((field) => field.fieldname === fieldname)
  if (index !== -1) {
    fields.value.splice(index, 1) // Remove the field at the found index
  }
}

// Method to delete a section only (removes the section break)
export function deleteSection(fields, section) {
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (sectionIndex !== -1) {
    deleteField(fields, section) // Delete the section break
  }
}

// Method to delete a section with all its columns and fields
export function deleteSectionWithContent(fields, section) {
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (sectionIndex !== -1) {
    // Remove the section break
    fields.value.splice(sectionIndex, 1)

    // Iterate to find and remove all fields and columns in this section
    let nextIndex = sectionIndex

    while (nextIndex < fields.value.length) {
      if (fields.value[nextIndex].fieldtype === 'Section Break') {
        break // Stop at the next section
      }
      fields.value.splice(nextIndex, 1) // Remove the field/column
    }
  }
}

// Method to delete a column only (removes the column break)
export function deleteColumn(fields, section, column) {
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (sectionIndex !== -1) {
    const columnIndex = fields.value.findIndex(
      (field) =>
        field.fieldtype === 'Column Break' && field.fieldname === column,
    )

    if (columnIndex !== -1) {
      deleteField(fields, column) // Remove the column break
    }
  }
}

// Method to delete a column with all its fields
export function deleteColumnWithContent(fields, section, column) {
  const sectionIndex = fields.value.findIndex(
    (field) =>
      field.fieldtype === 'Section Break' && field.fieldname === section,
  )

  if (sectionIndex !== -1) {
    const columnIndex = fields.value.findIndex(
      (field) =>
        field.fieldtype === 'Column Break' && field.fieldname === column,
    )

    if (columnIndex !== -1) {
      // Remove the column break
      fields.value.splice(columnIndex, 1)

      // Iterate to remove all fields below this column
      let nextIndex = columnIndex

      while (nextIndex < fields.value.length) {
        if (
          fields.value[nextIndex].fieldtype === 'Column Break' ||
          fields.value[nextIndex].fieldtype === 'Section Break'
        ) {
          break // Stop at the next column or section
        }
        fields.value.splice(nextIndex, 1) // Remove the field
      }
    }
  }
}

// Check if the given field is selected or not
export function isSelected(selectedField, current_fieldname) {
  return selectedField && selectedField.fieldname === current_fieldname
}

export function transformFields(fields) {
  const groupBySection = {}
  let curr_section = ''
  let curr_column = ''

  fields.forEach((field) => {
    switch (field.fieldtype) {
      case 'Section Break':
        curr_section = field.fieldname
        if (!groupBySection[curr_section]) {
          groupBySection[curr_section] = { column_count: 0, columns: {} }
        }
        curr_column = '' // Reset current column when a new section starts
        break

      case 'Column Break':
        curr_column = field.fieldname
        if (!groupBySection[curr_section].columns[curr_column]) {
          groupBySection[curr_section].column_count += 1
          groupBySection[curr_section].columns[curr_column] = []
        }
        break

      default:
        if (!groupBySection[curr_section]) {
          groupBySection[curr_section] = { column_count: 0, columns: {} }
        }
        if (!groupBySection[curr_section].columns[curr_column]) {
          groupBySection[curr_section].column_count += 1
          groupBySection[curr_section].columns[curr_column] = []
        }
        groupBySection[curr_section].columns[curr_column].push(field)
        break
    }
  })

  return groupBySection
}

export function getFieldIndex(fields, fieldname) {
  return fields.findIndex((field) => field.fieldname === fieldname)
}
