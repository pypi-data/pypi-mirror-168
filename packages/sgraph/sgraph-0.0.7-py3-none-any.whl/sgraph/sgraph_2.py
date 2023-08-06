
# selement.py
#   attrs: dict[str, sattribute]
#   inbound: selementassociation*
#   undirected: sundirectedelementassociation*
#   outbound: selmeentassociation*
# selementassociation.py
#    inbound: selement
#    outbound: selement
#    attrs: dict[str, sattribute]
# sundirectedelementassociation.py
#    connected: selement*
#    attrs: dict[str, sattribute]
# sattribute:
#    value: primitive types or None if element is preferred
#    data_type: str, int, foo...
#    element: selement?
#    attrs: dict[str, attribute]

