export interface ASTNode {
    type: string,
    value?: string | number,
    name_token?: any,
    operator?: string,
    input_token?: any,

    left?: ASTNode,
    right?: ASTNode,
    expression?: ASTNode,
    condition?: ASTNode,
    body?: ASTNode[],
    statements?: ASTNode[]
}

export interface D3Node {
    name: string,
    attributes?: Record<string,string | number>,
    children?: D3Node[]
}