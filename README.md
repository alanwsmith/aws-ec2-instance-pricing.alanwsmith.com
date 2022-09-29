# aws-ec2-instance-pricing.alanwsmith.com

A quick script to look at specific EC2 pricing
for projects.

This isn't dynamic so the website isn't up to date.
but you can pull the code from github and run it
yourself (using your credentails)

If you're looking for list stuff, [this one](https://instances.vantage.sh/)
looks solid. I wanted to sort and filter in ways
it didn't do which is why I'm building my own
thing.

## Notes

- The `scripts/list_aws_services/list_aws_services.py`
  pulls a list of the AWS services and the attributes
  you can query. I only need EC2 right now. Since it
  was just as easy to grab the full list I did.

- The pricing script gets raw data for Linux machines in the  
  us-east-1 region. It only pulls that once since there's
  a lot of it and it times some time. The second script
  in there process that data to produce the price list.

## References

- https://aws.amazon.com/ec2/pricing/
- https://instances.vantage.sh/
- https://awscli.amazonaws.com/v2/documentation/api/latest/reference/pricing/get-products.html
- https://docs.aws.amazon.com/cli/latest/reference/pricing/index.html
- https://aws.amazon.com/ec2/instance-types/
- https://aws.amazon.com/ec2/pricing/on-demand/
- https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_pricing_GetProducts.html
- https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_pricing_Filter.html
-
