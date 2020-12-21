Book of Knowledge
===

Machine Learning Project to obtain market predictions for the company Textil Santanderina.
---

- This document is going to be used to sum up all the inner knowledge we have about or raw data, in order is easy to consult in the future, just for getting started we let here for us a reminder of all data dimensions. Also, we see clearly that a reduction of dimensions is going to be necessary, as far as we have too many variables (columns) which are an 
obstacle in performing effective ML models. So, we work with: 

-Variables: 34 different columns. 
 
-Number of observations: rows, to determine in the future, but it seems is going to be ok.

Now, we start describing the meaning of our different variables, we know them thanks to the explanation made by Antonio Rábago.
---

### TipoDOC (First column), categorial variable:

Values:

-**F**: commercial invoice, it has n lines (money goes in).
-**A**: payment, it could have multiple lines as well (money goes out).

### Identificatory columns, both are int variables:

-**B, Documento**: id of the document.
-**D, Factura**: id of the commercial invoice, note that its equal to the column **Documento** when our TipoDoc is **F**, and it is different when we are working with **payments**, because those payments are related to articles demanded previously which are returned by the client, these two columns could be very useful in order to separate lines from one document of the other, and to associate payments with past invoices.

### LineDoc, int variable:

-Is our column to distinguish how many lines has a document, **note that a payment (abono) could be only applied in one of the lines of an invoice (Factura)**. We are going to call the lines in the commercial invoices as **orders (Pedidos in Spanish) **.

### Fecha (date of the commercial invoice):

-Just note that could be a good idea **to add the variable fabrication date**, could be a very important variable in order to analyse productivity peaks more than sell peaks.

### TipoOperacion (column K), categorical variable:

Values:

-**Venta**: this value means that the operation was a commercial invoice, in this concrete case the information which provides us this column is redundant (just looking at TipoDoc we already know is a **Factura**).
-**Devol.Mercanc.Defectos**: the product from a concrete order is returned by the client firm, this value could be interesting to try to monitor quality state in the our productions.
-**Producto defectuoso**.
-**Muestras**.
-**Devolución de mercancia**.
-Note that new reasons could be introduced as new possible values of the variable.

### AfectaCantidad (column L), Boolean variable:

-It indicates us if the order (Pedido) affects the quantity of product we have, in a commercial invoice obviously yes, but in a payment is not always the case.

### MetroPieza (Column AE) + Cantidad (Column M), both are numeric variables:

Any commercial invoice its composed by different pieces (inside a lot), if we sum all the quantities from the same lot in AE we obtain the total quantity (Cantidad) given by the column M.

### Precio (column O), float:

-Just the price currency/metre. Just note that could be 0 in case that is a sample the company sends to a client (they need receipt anyway).

### Moneda (column P), string:

-Currency of the operation.

### Cambio (column Q), float:

-Conversion factor which measures the relation €/ foreign currency (in case of € the **exchange rate** is equal to 1).

### Importe (column R), float:

-Price in euro after using the conversion factor. Very easy to note than **Quantity (Cantidad) * Price (Precio) * ExchangeRate (Cambio)= Total amount (Importe)**

### CodigoArticulo (column S), int:

-Unique code for any type of product.

### Variables related to the product itself: now we will talk about a set of variables which makes possible how to distinguish between products and its characteristics, from the column U to the Z: Serie (Serie), Acabado(finish), Estampado(print), Combinacion(Combination), Color(Colour) y Ancho (width). Note than in the cases of the print, the combination and colour, 0 means NULL.

### CN8(column AA), int:

-Does not seem to be important information, just another identifier.

### MetrosDefectuosos (column AG), float:

-Indicates us the number of metres which does not accomplish the quality standards. This could be an interesting case due to the fact that the main part of the rows are going to have value 0, then the probability of having no defective metres is positive (modelo de solucion esquina de Tobit) 

