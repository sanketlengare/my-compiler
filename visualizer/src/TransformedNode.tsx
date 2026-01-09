import { ASTNode,D3Node } from "./types";

export function TransformAST(astNode: ASTNode): D3Node | null {
    if (!astNode) {
        return null;
    }

    const d3Node: D3Node = {
        name: astNode.type,
        attributes: {},
        children: []
    };

    if (astNode.value !== undefined && astNode.value !== null) {
        if (typeof astNode.value === 'object') {
            const childNode = TransformAST(astNode.value as unknown as ASTNode);
            if (childNode) d3Node.children!.push(childNode);
        } else {
            d3Node.attributes!.value = astNode.value;
        }
    }

    if (astNode.name_token) {
        const token = astNode.name_token;
        d3Node.attributes!.var = (typeof token === 'object') ? token.text : token;
    }

    if (astNode.input_token) {
        const token = astNode.input_token;
        d3Node.attributes!.input = (typeof token === 'object') ? token.text : token;
    }

    if (astNode.operator) {
        d3Node.attributes!.operator = astNode.operator;
    }

    const singleNodes = [astNode.left,astNode.right,astNode.expression,astNode.condition];

    singleNodes.forEach(child => {
        if (child) {
            const transformed = TransformAST(child);

            if (transformed) {
                d3Node.children!.push(transformed);
            }
        }
    });

    if (astNode.body) {
        astNode.body.forEach(child => {
            const transformed = TransformAST(child);

            if (transformed) {
                d3Node.children!.push(transformed);
            }
        });
    }

    if (astNode.statements) {
        astNode.statements.forEach(child => {
            const transformed = TransformAST(child);

            if (transformed) {
                d3Node.children!.push(transformed);
            }
        });
    }

    if (d3Node.children?.length === 0) {
        delete d3Node.children
    }

    console.log(d3Node)

    return d3Node;
}


export function renderCustomNode({ nodeDatum,toggleNode }: any) {
    let nodeColor = "#00d8ff"; // Default Cyan
    if (["Program","While","If","Goto","Label","Repeat"].includes(nodeDatum.name)) nodeColor = "#bd93f9"; // Purple
    if (["Num","Float","String"].includes(nodeDatum.name)) nodeColor = "#50fa7b"; // Green
    if (["Bin_Op"].includes(nodeDatum.name)) nodeColor = "#ff79c6"; // Pink
    if (["Let","Input","Print"].includes(nodeDatum.name)) nodeColor = "#8be9fd"; // Cyan

    let infoText = "";
    if (nodeDatum.attributes?.value) infoText = String(nodeDatum.attributes.value);
    else if (nodeDatum.attributes?.operator) infoText = String(nodeDatum.attributes.operator);
    else if (nodeDatum.attributes?.var) infoText = String(nodeDatum.attributes.var);
    else if (nodeDatum.attributes?.input) infoText = String(nodeDatum.attributes.input);

    return (
        <g>
            <circle
                r="15"
                fill={nodeColor}
                stroke="#ffffff"
                strokeWidth="2"
                onClick={toggleNode}
                style={{ cursor: 'pointer' }}
            />

            <text
                fill="white"
                strokeWidth="0"
                x="25"
                dy="-5"
                fontSize="14px"
                fontWeight="bold"
                style={{ textShadow: '1px 1px 2px black' }}
            >
                {nodeDatum.name}
            </text>

            {infoText && (
                <text
                    fill="#f1fa8c"
                    strokeWidth="0"
                    x="25"
                    dy="15"
                    fontSize="12px"
                    fontFamily="monospace"
                >
                    {infoText}
                </text>
            )}
        </g>
    );
};
