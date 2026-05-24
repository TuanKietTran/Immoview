import * as cdk from "aws-cdk-lib";
import { RealEstateStack } from "../lib/real-estate-stack";

const app = new cdk.App();
new RealEstateStack(app, "RealEstateStack", {
  env: { region: "eu-central-1", account: "000000000000" },
});
