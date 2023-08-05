import dynamic from "next/dynamic"
import ElementsLoading from "../../ElementsLoading"

const elements: ElementsRecord = {
  InnerHTML: dynamic(() => import("dangerously-set-html-content"), { loading: ElementsLoading, ssr: false }),
}


const loadInnerHTML: ElementsLoader = element => elements[element]

export default loadInnerHTML
