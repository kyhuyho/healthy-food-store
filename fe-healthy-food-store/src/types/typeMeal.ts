export interface IMeal {
  _id: string;
  name: string;
  weight: number;
  price: number;
  calo: number;
  protein: number;
  fat: number;
  satFat: number;
  transFat: number;
  carb: number;
  fiber: number;
  sugar: number;
  cholesterol: number;
  sodium: number;
  calcium: number;
  iron: number;
  zinc: number;
  desc: string;
  quantity: number;
  kind: string;
  ingredients: {
    ingredient: { _id: string; name: string };
  }[];
  image: string;
}