import { useState, useEffect } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [resource, setResource] = useState('clientes')
  const [data, setData] = useState([])
  const [clientes, setClientes] = useState([])
  const [productos, setProductos] = useState([])
  const [formData, setFormData] = useState({})
  const [editId, setEditId] = useState(null)
  const [detallesTemp, setDetallesTemp] = useState([])

  useEffect(() => {
    fetchData(resource)
    if(resource === 'pedidos') fetchData('clientes')
    if(resource === 'detalles-pedido') {
      fetchData('pedidos')
      fetchData('productos')
    }
  }, [resource])

  const fetchData = async (endpoint) => {
    const response = await fetch(`${API_URL}/${endpoint}/`)
    const result = await response.json()
    
    if(endpoint === 'clientes') setClientes(result)
    else if(endpoint === 'productos') setProductos(result)
    else if(endpoint === resource) setData(result)  // Fixed empty string check
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const url = editId ? `${API_URL}/${resource}/${editId}/` : `${API_URL}/${resource}/`
    const method = editId ? 'PUT' : 'POST'

    const bodyData = resource === 'pedidos' ? {  // Fixed typo from 'pedido' to 'pedidos'
      cliente: formData.cliente,
      total: detallesTemp.reduce((acc, detalle) => 
        acc + (detalle.cantidad * productos.find(p => p.id == detalle.producto)?.precio || 0), 0)
    } : formData
    
    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        console.error('API Error:', errorData)
        return
      }

      if (resource === 'pedidos' && !editId) {
        const pedido = await response.json()
        await Promise.all(detallesTemp.map(detalle => 
          fetch(`${API_URL}/detalles-pedido/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              pedido: pedido.id,
              producto: detalle.producto,
              cantidad: detalle.cantidad
            })
          })
        ))
      }

      resetForm()
      fetchData(resource)
    } catch (error) {
      console.error('Network Error:', error)
    }
  }

  const handleDelete = async (id) => {
    if(window.confirm('¿Estás seguro de eliminar este registro?')) {
      await fetch(`${API_URL}/${resource}/${id}/`, { method: 'DELETE' })
      fetchData(resource)
    }
  }

  const handleEdit = (item) => {
    setEditId(item.id)
    setFormData(item)
    if(resource === 'pedidos') setDetallesTemp(item.detalles)
  }

  const resetForm = () => {
    setFormData({})
    setEditId(null)
    setDetallesTemp([])
  }

  const addDetalle = () => {
    setDetallesTemp([...detallesTemp, { producto: '', cantidad: 1 }])
  }

  const updateDetalle = (index, field, value) => {
    const updated = [...detallesTemp]
    updated[index][field] = value
    setDetallesTemp(updated)
  }

  return (
    <div className="container">
      <nav className="nav-tabs">
        {['clientes', 'productos', 'pedidos', 'detalles-pedido'].map((tab) => (
          <button
            key={tab}
            className={resource === tab ? 'active' : ''}
            onClick={() => setResource(tab)}
          >
            {tab.toUpperCase()}
          </button>
        ))}
      </nav>

      <form onSubmit={handleSubmit} className="form-container">
        <h2>{editId ? 'Editar' : 'Nuevo'} {resource.slice(0, -1)}</h2>
        
        {resource === 'clientes' && (
          <>
            <input
              placeholder="Nombre"
              value={formData.nombre || ''}
              onChange={(e) => setFormData({...formData, nombre: e.target.value})}
              required
            />
            <input
              placeholder="Teléfono"
              value={formData.telefono || ''}
              onChange={(e) => setFormData({...formData, telefono: e.target.value})}
            />
            <textarea
              placeholder="Dirección"
              value={formData.direccion || ''}
              onChange={(e) => setFormData({...formData, direccion: e.target.value})}
            />
          </>
        )}

        {resource === 'productos' && (
          <>
            <input
              placeholder="Nombre"
              value={formData.nombre || ''}
              onChange={(e) => setFormData({...formData, nombre: e.target.value})}
              required
            />
            <textarea
              placeholder="Descripción"
              value={formData.descripcion || ''}
              onChange={(e) => setFormData({...formData, descripcion: e.target.value})}
            />
            <input
              type="number"
              step="0.01"
              placeholder="Precio"
              value={formData.precio || ''}
              onChange={(e) => setFormData({...formData, precio: parseFloat(e.target.value)})}
              required
            />
          </>
        )}

{resource === 'pedidos' && (
    <>
      <select
        value={formData.cliente || ''}
        onChange={(e) => setFormData({...formData, cliente: e.target.value})}
        required
      >
        <option value="">Seleccionar Cliente</option>
        {clientes.map((cliente) => (
          <option key={cliente.id} value={cliente.id}>{cliente.nombre}</option>
        ))}
      </select>
      
      <div className="detalles-container">
        <button type="button" onClick={addDetalle}>Agregar Producto</button>
        {detallesTemp.map((detalle, index) => (
          <div key={index} className="detalle-item">
            <select
              value={detalle.producto}
              onChange={(e) => updateDetalle(index, 'producto', e.target.value)}
            >
              <option value="">Seleccionar Producto</option>
              {productos.map((producto) => (
                <option key={producto.id} value={producto.id}>{producto.nombre}</option>
              ))}
            </select>
            <input
              type="number"
              value={detalle.cantidad}
              onChange={(e) => updateDetalle(index, 'cantidad', parseInt(e.target.value))}
              min="1"
            />
          </div>
        ))}
      </div>
    </>  
  )}

        {resource === 'detalles-pedido' && (
          <>
            <select
              value={formData.pedido || ''}
              onChange={(e) => setFormData({...formData, pedido: e.target.value})}
              required
            >
              <option value="">Seleccionar Pedido</option>
              {data.map((pedido) => (
                <option key={pedido.id} value={pedido.id}>Pedido #{pedido.id}</option>
              ))}
            </select>
            <select
              value={formData.producto || ''}
              onChange={(e) => setFormData({...formData, producto: e.target.value})}
              required
            >
              <option value="">Seleccionar Producto</option>
              {productos.map((producto) => (
                <option key={producto.id} value={producto.id}>{producto.nombre}</option>
              ))}
            </select>
            <input
              type="number"
              min="1"
              value={formData.cantidad || ''}
              onChange={(e) => setFormData({...formData, cantidad: parseInt(e.target.value)})}
              required
            />
          </>
        )}

        <div className="form-actions">
          <button type="submit">Guardar</button>
          <button type="button" onClick={resetForm}>Cancelar</button>
        </div>
      </form>

      <div className="data-table">
        <table>
          <thead>
            <tr>
              {data[0] && Object.keys(data[0]).map((key) => (
                <th key={key}>{key.toUpperCase()}</th>
              ))}
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
          {data.map((item) => (
  <tr key={item.id}>
    {Object.entries(item).map(([key, value], index) => (
      <td key={index}>
        {Array.isArray(value) ? (
          // Handle array of detalles
          value.map(detalle => 
            `${productos.find(p => p.id === detalle.producto)?.nombre || 'Producto'} x ${detalle.cantidad}`
          ).join(', ')
        ) : typeof value === 'object' ? (
          // Handle single object relationship
          value?.nombre || value?.id || JSON.stringify(value)
        ) : (
          // Simple values
          value
        )}
      </td>
    ))}
    <td>
      <button onClick={() => handleEdit(item)}>Editar</button>
      <button onClick={() => handleDelete(item.id)}>Eliminar</button>
    </td>
  </tr>
))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App