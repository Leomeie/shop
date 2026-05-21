function normalizeErrors(value) {
  if (!value) return []
  if (Array.isArray(value)) return value.map((item) => String(item))
  return [String(value)]
}

function pickFirstLine(lines, fallback = '') {
  return lines.length ? lines[0] : fallback
}

export function validateLoginForm(form) {
  const fieldErrors = {}
  const summaryLines = []

  const username = (form.username || '').trim()
  const password = form.password || ''

  if (!username) {
    fieldErrors.username = '请输入用户名'
    summaryLines.push('用户名不能为空')
  } else if (username.length < 3) {
    fieldErrors.username = '用户名至少需要 3 个字符'
    summaryLines.push('用户名长度太短')
  }

  if (!password) {
    fieldErrors.password = '请输入密码'
    summaryLines.push('密码不能为空')
  } else if (password.length < 6) {
    fieldErrors.password = '密码至少需要 6 个字符'
    summaryLines.push('密码长度太短')
  }

  return {
    valid: Object.keys(fieldErrors).length === 0,
    fieldErrors,
    summaryLines,
  }
}

export function validateRegisterForm(form) {
  const fieldErrors = {}
  const summaryLines = []

  const username = (form.username || '').trim()
  const password = form.password || ''
  const passwordConfirm = form.password_confirm || ''

  if (!username) {
    fieldErrors.username = '请输入用户名'
    summaryLines.push('用户名不能为空')
  } else if (username.length < 3) {
    fieldErrors.username = '用户名至少需要 3 个字符'
    summaryLines.push('用户名长度太短')
  } else if (username.length > 20) {
    fieldErrors.username = '用户名不能超过 20 个字符'
    summaryLines.push('用户名过长')
  } else if (!/^[A-Za-z0-9_]+$/.test(username)) {
    fieldErrors.username = '用户名只能包含字母、数字或下划线'
    summaryLines.push('用户名包含不支持的字符')
  }

  if (!password) {
    fieldErrors.password = '请输入密码'
    summaryLines.push('密码不能为空')
  } else if (password.length < 6) {
    fieldErrors.password = '密码至少需要 6 个字符'
    summaryLines.push('密码长度太短')
  } else if (password.length > 20) {
    fieldErrors.password = '密码不能超过 20 个字符'
    summaryLines.push('密码过长')
  }

  if (!passwordConfirm) {
    fieldErrors.password_confirm = '请再次输入密码'
    summaryLines.push('确认密码不能为空')
  } else if (password !== passwordConfirm) {
    fieldErrors.password_confirm = '两次输入的密码不一致'
    summaryLines.push('两次输入的密码不一致')
  }

  return {
    valid: Object.keys(fieldErrors).length === 0,
    fieldErrors,
    summaryLines,
  }
}

export function parseAuthApiError(error, mode = 'login') {
  const payload = error || {}
  const errors = payload.errors || {}
  const fieldErrors = {}
  const summaryLines = []

  if (errors.username) fieldErrors.username = pickFirstLine(normalizeErrors(errors.username))
  if (errors.password) fieldErrors.password = pickFirstLine(normalizeErrors(errors.password))
  if (errors.password_confirm) fieldErrors.password_confirm = pickFirstLine(normalizeErrors(errors.password_confirm))

  const nonFieldErrors = normalizeErrors(errors.non_field_errors)
  if (nonFieldErrors.length) summaryLines.push(...nonFieldErrors)

  if (payload.message && !summaryLines.includes(payload.message)) {
    summaryLines.unshift(payload.message)
  }

  if (mode === 'login') {
    summaryLines.push('请确认用户名是否填写正确，并注意大小写。')
    summaryLines.push('请确认密码是否完整输入，且没有多余空格。')
    summaryLines.push('管理员请使用用户名登录，例如：admin。')
  } else {
    summaryLines.push('用户名需为 3-20 位，只能包含字母、数字或下划线。')
    summaryLines.push('密码需为 6-20 位，并与确认密码保持一致。')
    summaryLines.push('如果提示用户名已存在，请更换一个新的用户名。')
  }

  return {
    fieldErrors,
    summaryLines: Array.from(new Set(summaryLines.filter(Boolean))),
  }
}
