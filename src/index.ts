import { Hono } from 'hono'
const app = new Hono()

import { cors } from 'hono/cors'
app.use(cors())

app.get('/', c => {
    return c.text('my vercel tiny apis')
})

app.all('/proxy', async c => {
    const url = c.req.query('url')
    if (!url) return c.body(null, 404)

    const method = c.req.method
    const { host, 'content-length': cl, 'content-encoding': ce, ...headers } = c.req.header()
    const body = method !== 'GET' && method !== 'HEAD' ? await c.req.arrayBuffer() : undefined

    const response = await fetch(url, {
        method,
        headers: {
            ...headers,
            'accept-encoding': 'identity'
        },
        body: body as any
    })

    const newHeaders = new Headers(response.headers)
    newHeaders.delete('content-encoding')
    newHeaders.delete('content-length')

    return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders
    })
})

app.get('/replace', async c => {
    const url = c.req.query('url')
    if (!url) return c.body(null, 404)

    const oldStr = c.req.query('old')
    if (!oldStr) return c.body(null, 404)

    const newStr = c.req.query('new')
    if (!newStr) return c.body(null, 404)

    const response = await fetch(url)
    const text = await response.text()

    return c.text(text.replaceAll(oldStr, newStr))
})

export default app
